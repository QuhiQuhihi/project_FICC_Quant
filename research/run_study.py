"""Run a complete numerical curve-to-hedge study; no market-price claims."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import numpy as np
import pandas as pd
import QuantLib as ql
from research.pricing import (
    DATE,
    CAL,
    fixture,
    curves,
    bond,
    swap,
    value,
    bumped,
    quote_risk,
    fx_forward,
    valuation_date,
)
from research.common import ROOT, RESULTS, FIGURES, table, plot_style, write_metadata


def main():
    RESULTS.mkdir(exist_ok=True)
    with valuation_date():
        q = fixture()
        d, p, residuals = curves(q)
        b, bcf = bond(d)
        s, scf, coupon = swap(d, p)
        flows = pd.concat([bcf, scf])
        flows.to_csv(RESULTS / "cashflows.csv", index=False)
        residuals.to_csv(RESULTS / "calibration.csv", index=False)
        reconciliation = pd.DataFrame(
            [
                {
                    "instrument": "bond",
                    "quantlib_pv": b.NPV(),
                    "independent_pv": bcf.pv.sum(),
                    "residual": b.NPV() - bcf.pv.sum(),
                    "clean": b.cleanPrice(),
                    "accrued": b.accruedAmount(),
                    "dirty": b.dirtyPrice(),
                },
                {
                    "instrument": "payer_swap",
                    "quantlib_pv": s.NPV(),
                    "independent_pv": scf.pv.sum(),
                    "residual": s.NPV() - scf.pv.sum(),
                    "clean": np.nan,
                    "accrued": np.nan,
                    "dirty": np.nan,
                },
            ]
        )
        reconciliation.to_csv(RESULTS / "valuation.csv", index=False)
        if residuals.residual.abs().max() > 1e-8 or reconciliation.residual.abs().max() > 1e-8:
            raise ValueError("Calibration/cash-flow reconciliation failed")
        nodes = []
        for month in range(1, 121):
            date = CAL.advance(DATE, ql.Period(month, ql.Months))
            t = ql.Actual365Fixed().yearFraction(DATE, date)
            if date > min(d.maxDate(), p.maxDate()):
                continue
            nodes.append(
                {
                    "date": date.ISO(),
                    "years": t,
                    "discount_df": d.discount(date),
                    "projection_df": p.discount(date),
                    "discount_zero": -np.log(d.discount(date)) / t,
                    "projection_zero": -np.log(p.discount(date)) / t,
                    "discount_forward": d.forwardRate(
                        date, date, ql.Actual365Fixed(), ql.Continuous
                    ).rate(),
                }
            )
        nodes = pd.DataFrame(nodes)
        nodes.to_csv(RESULTS / "curve_nodes.csv", index=False)
        risk = []
        for bump in [0.1, 1.0, 5.0]:
            dv, cx = quote_risk(q, coupon, bump)
            for j, name in enumerate(["bond", "payer_swap"]):
                risk.append(
                    {
                        "instrument": name,
                        "bump_bps": bump,
                        "signed_dv01": dv[j],
                        "currency_per_bp_squared": cx[j],
                    }
                )
        pd.DataFrame(risk).to_csv(RESULTS / "bump_convergence.csv", index=False)
        dv, cx = quote_risk(q, coupon)
        hedge = -dv[0] / dv[1]
        base = value(q, coupon)
        buckets = []
        for curve in ["ois_rate", "term_rate"]:
            for i in range(len(q)):
                up = q.copy()
                down = q.copy()
                up.loc[i, curve] += 1e-4
                down.loc[i, curve] -= 1e-4
                v = (value(up, coupon) - value(down, coupon)) / 2
                buckets.append(
                    {
                        "curve": curve,
                        "years": int(q.years.iloc[i]),
                        "bond": v[0],
                        "swap": v[1],
                        "hedged": v[0] + hedge * v[1],
                    }
                )
        buckets = pd.DataFrame(buckets)
        buckets.to_csv(RESULTS / "quote_buckets.csv", index=False)
        scenarios = {
            "parallel_up100": np.full(10, 0.01),
            "parallel_down100": np.full(10, -0.01),
            "steepener": np.linspace(-0.005, 0.005, 10),
            "flattener": np.linspace(0.005, -0.005, 10),
            "local_7y": np.eye(10)[6] * 0.01,
        }
        pnl = []
        for name, shock in scenarios.items():
            change = value(bumped(q, shock, shock), coupon) - base
            first = sum(
                (g.bond + hedge * g.swap).to_numpy() @ (shock * 1e4)
                for _, g in buckets.groupby("curve")
            )
            second = (
                (dv[0] + hedge * dv[1]) * shock[0] * 1e4
                + 0.5 * (cx[0] + hedge * cx[1]) * (shock[0] * 1e4) ** 2
                if name.startswith("parallel")
                else np.nan
            )
            pnl.append(
                {
                    "scenario": name,
                    "unhedged_bond_pnl": change[0],
                    "swap_pnl_per100": change[1],
                    "hedged_pnl": change[0] + hedge * change[1],
                    "bucket_first_order": first,
                    "parallel_second_order": second,
                }
            )
        pnl = pd.DataFrame(pnl)
        pnl.to_csv(RESULTS / "scenario_pnl.csv", index=False)
        pd.DataFrame(
            [
                {
                    "bond_face": 100,
                    "swap_notional_per100_bond": 100 * hedge,
                    "swap_units": hedge,
                    "fixed_coupon": coupon,
                    "bond_signed_quote_dv01": dv[0],
                    "swap_signed_quote_dv01": dv[1],
                    "hedged_signed_quote_dv01": dv[0] + hedge * dv[1],
                }
            ]
        ).to_csv(RESULTS / "hedge.csv", index=False)
        # Independent derivative of explicit bond CFs under a continuous zero spread.
        times = np.array(
            [ql.Actual365Fixed().yearFraction(DATE, ql.DateParser.parseISO(x)) for x in bcf.date]
        )
        pv = bcf.pv.to_numpy()
        analytical = -np.sum(times * pv) * 1e-4
        spread_plus = ql.ZeroSpreadedTermStructure(
            ql.YieldTermStructureHandle(d), ql.QuoteHandle(ql.SimpleQuote(1e-4))
        )
        spread_minus = ql.ZeroSpreadedTermStructure(
            ql.YieldTermStructureHandle(d), ql.QuoteHandle(ql.SimpleQuote(-1e-4))
        )
        central = (bond(spread_plus)[0].NPV() - bond(spread_minus)[0].NPV()) / 2
        pd.DataFrame(
            [
                {
                    "zero_spread_analytic_dv01": analytical,
                    "zero_spread_central_dv01": central,
                    "difference": central - analytical,
                    "quote_dv01_different_object": dv[0],
                }
            ]
        ).to_csv(RESULTS / "independent_risk.csv", index=False)
        conventions = []
        for name, kw in [
            ("dual_logdiscount", {}),
            ("single_curve", {"single": True}),
            ("linear_zero", {"interpolation": "linear_zero"}),
            ("bond_act360", {"bond_dc": ql.Actual360()}),
        ]:
            v = value(q, coupon, **kw)
            conventions.append(
                {
                    "case": name,
                    "bond_pv": v[0],
                    "swap_pv": v[1],
                    "bond_difference": v[0] - base[0],
                    "swap_difference": v[1] - base[1],
                }
            )
        conventions = pd.DataFrame(conventions)
        conventions.to_csv(RESULTS / "convention_effects.csv", index=False)
        fxdate = CAL.advance(DATE, ql.Period(1, ql.Years))
        t = ql.Actual365Fixed().yearFraction(DATE, fxdate)
        usd = d.discount(fxdate)
        eur = np.exp(-0.025 * t)
        fwd = fx_forward(1.10, usd, eur)
        pd.DataFrame(
            [
                {
                    "quote": "USD per EUR",
                    "spot": 1.10,
                    "maturity": fxdate.ISO(),
                    "usd_discount": usd,
                    "eur_discount": eur,
                    "fair_forward": fwd,
                    "usd_pv_at_fair": 1.10 * eur - fwd * usd,
                    "usd_pv_strike_plus_1cent": 1.10 * eur - (fwd + 0.01) * usd,
                    "assumption": "zero basis; compatible collateral; illustrative EUR curve",
                }
            ]
        ).to_csv(RESULTS / "fx_parity.csv", index=False)
        plt = plot_style()
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        nodes.plot(
            x="years", y=["discount_zero", "projection_zero", "discount_forward"], ax=axes[0]
        )
        axes[0].set(
            ylabel="Continuous annual rate",
            xlabel="Years",
            title="Illustrative curves, 15 Sep 2026",
        )
        nodes.plot(x="years", y=["discount_df", "projection_df"], ax=axes[1])
        axes[1].set(
            ylabel="Discount factor", xlabel="Years", title="Positive factors; no market quotes"
        )
        fig.tight_layout()
        fig.savefig(FIGURES / "curves.png", dpi=150)
        plt.close(fig)
        fig, ax = plt.subplots()
        residuals.assign(residual_bp=residuals.residual * 1e4).pivot(
            index="years", columns="curve", values="residual_bp"
        ).plot.bar(ax=ax)
        ax.set(
            ylabel="Implied minus input quote (bp)",
            xlabel="Quoted tenor (years)",
            title="Bootstrap calibration residuals",
        )
        fig.tight_layout()
        fig.savefig(FIGURES / "calibration.png", dpi=150)
        plt.close(fig)
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
        for ax, (name, g) in zip(axes, buckets.groupby("curve")):
            g.plot.bar(x="years", y=["bond", "swap", "hedged"], ax=ax)
            ax.set(
                title=name,
                xlabel="Quote tenor (years)",
                ylabel="Signed currency / +1 bp per 100 bond",
            )
        fig.tight_layout()
        fig.savefig(FIGURES / "risk.png", dpi=150)
        plt.close(fig)
        fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
        labels = pnl.set_index("scenario").rename(
            columns={
                "unhedged_bond_pnl": "Unhedged bond",
                "hedged_pnl": "Hedged revaluation",
                "bucket_first_order": "Bucket approximation",
            }
        )
        labels[["Unhedged bond", "Hedged revaluation"]].plot.barh(ax=axes[0])
        labels[["Hedged revaluation", "Bucket approximation"]].plot.barh(
            ax=axes[1], color=["#bc6c25", "#718355"]
        )
        for ax, title in zip(axes, ["Unhedged and hedged P&L", "Hedge residuals (expanded scale)"]):
            ax.axvline(0, color="#555", lw=0.7)
            ax.set(xlabel="Instantaneous USD P&L per 100 bond", ylabel="", title=title)
        fig.suptitle("Frozen hedge; illustrative 15 September 2026 curves; different panel scales")
        fig.tight_layout()
        fig.savefig(FIGURES / "hedge.png", dpi=150)
        plt.close(fig)
        maxres = float(pnl.hedged_pnl.abs().max())
        largest = pnl.loc[pnl.hedged_pnl.abs().idxmax(), "scenario"]
        findings = (
            f"""# Curves, conventions and the limits of a one-swap hedge\n\nUnder the explicit illustrative inputs, a bond priced at **{base[0]:.6f} per 100** is parallel-DV01-neutralized with **{hedge:.6f} units** of a payer swap (each unit has notional 100). The largest absolute residual among five frozen instantaneous scenarios is **{maxres:.6f} per 100**, in **{largest}**. A single parallel hedge leaves curve-shape and convexity risk.\n\nThese are numerical model results from constructed quotes dated 15 September 2026. No residual is an observed mispricing or executable trading opportunity.\n\n## Independent valuation and calibration\n\n"""
            + table(reconciliation)
            + f"""\nMaximum quote repricing error is {residuals.residual.abs().max():.3g} in decimal rate units; maximum independent cash-flow PV discrepancy is {reconciliation.residual.abs().max():.3g} currency. Internal calibration accuracy is separate from market accuracy.\n\n## Controlled assumptions\n\n"""
            + table(conventions)
            + """\nThe term swap uses separate projection and discounting. Replacing its projection with OIS changes floating cash flows while the fixed coupon stays frozen. The bond day-count comparison changes coupon accrual; interpolation changes off-node values even when instruments calibrate.\n\n## Frozen hedge scenarios\n\n"""
            + table(pnl)
            + """\nQuote buckets are rebuilt-curve sensitivities, not zero-rate or yield-duration bumps. The bucket approximation is first order; the parallel second-order column is defined only for parallel shocks. Positions are held fixed, with no elapsed-time carry or cash flows.\n\n![Hedge residuals](../research/figures/hedge.png)\n\n## FX consistency\n\n"""
            + f"""With USD per EUR spot 1.10, the one-year illustrative fair forward is **{fwd:.6f} USD/EUR**. Its discounted cash-flow PV is zero to numerical tolerance under zero-basis, compatible-collateral assumptions. This verifies signs and parity, not executable cross-currency arbitrage.\n\nThe core is validated numerically. Live collateral, fixing, instrument and quote evidence is still required for a market study. Legacy options, CDS and cross-currency examples remain explicitly unvalidated archival context. See [conventions and methods](01-methods.md), [protocol](../research/PROTOCOL.md), [source register](../research/SOURCES.md), and [unrun extensions](../research/RESEARCH_AGENDA.md).\n"""
        )
        (ROOT / "docs/02-results.md").write_text(findings)
        readme = ROOT / "README.md"
        if readme.exists():
            parts = readme.read_text().split("\n\n", 2)
            readme.write_text(parts[0] + "\n\n" + findings.split("\n\n")[1] + "\n\n" + parts[2])
        (RESULTS / "headline.json").write_text(
            json.dumps(
                {
                    "bond_pv": base[0],
                    "hedge_units": hedge,
                    "maximum_absolute_hedged_pnl": maxres,
                    "scenario": largest,
                },
                indent=2,
            )
            + "\n"
        )
        write_metadata(
            {
                "valuation_date": DATE.ISO(),
                "quote_kind": "constructed illustrative",
                "QuantLib": ql.__version__,
                "tolerance": 1e-8,
            }
        )
        print(findings.split("\n\n")[1])


if __name__ == "__main__":
    main()
