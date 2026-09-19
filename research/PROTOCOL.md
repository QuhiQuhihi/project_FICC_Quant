# FICC numerical-validation protocol — 19 September 2026

Primary question: how much curve/convention risk remains after neutralizing parallel rate risk
with one swap? This is a constructed-input study, not observed mispricing or market calibration.
Dates and quotes below are assumptions fixed before valuation. The empirical quote objective
is not claimed complete: no independently documented executable OIS/term/basis set is supplied.

Valuation: 15 September 2026; USD; US GovernmentBond calendar; zero settlement days for
curve helpers and instruments so independent cash-flow checks share one reference date.
Bond begins 15 March 2026, matures 15 September 2033, 4% annual coupon, semiannual payments,
Actual/Actual ISMA, Modified Following, face 100. Exclude reference-date cash flows. This is a
synthetic bond, not a Treasury CUSIP; no credit/liquidity spread. Clean+accrued=dirty at valuation.

Discount curve: illustrative SOFR-style OIS par quotes for 1–10 years, annual fixed payments,
Actual/360, Modified Following, settlement zero; generated fixture rates 3.8%, 3.7%, 3.6%,
3.55%, 3.5%, 3.48%, 3.46%, 3.45%, 3.44%, 3.43%. Piecewise log-linear discount interpolation;
no extrapolation needed. Current overnight SOFR fixings are not substituted for this term curve.

Projection: synthetic USD 3M term index (not LIBOR), zero fixing lag, Actual/360, same calendar.
Annual fixed-leg swap quote helpers with those term-index conventions, fixed Actual/360,
quotes discount par rate +50 bp. Discount on the separate OIS curve. Single-curve counterfactual
uses OIS for both projection and discount. This pedagogical separation does not assert that a
particular traded index has a constant 50-bp spread or ignores basis in a live transaction.

Instrument: pay-fixed 7-year term swap, notional 100, annual fixed leg, quarterly floating,
forward-start one business day after valuation to avoid historical fixing dependencies. Set
fixed coupon to dual-curve fair rate, then freeze it across all sensitivities. No principal
exchange. Reconcile fixed and floating cash flows via independent accrual and discount formulas
against QuantLib at same settlement date. Restore evaluationDate after every independent run.

Primary numeric tolerances: helper repricing <1e-8 absolute quote rate; independent PV <1e-8
currency per 100; finite-difference DV01 changes across .1, 1, 5 bp within 1e-4 currency per bp.
Positive discounts required; monotonicity is not a universal no-arbitrage test in negative rates.

Signed DV01 = (PV(quotes+1bp)-PV(quotes-1bp))/2 in currency/bp, curves rebuilt. Both discount
and projection quote strips shift for parallel risk; report separate quote-bucket risks and a
parallel convexity measure. Also validate an independent continuous zero-spread bond derivative
-sum(t CF D)*1e-4 and distinguish its units/bumped object from quote DV01.

Hedge: bond plus h swaps, h=-bond parallel DV01/swap parallel DV01. Freeze positions. Revalue
instantaneous +100/-100 bp parallel shocks, linear -50/+50 bp steepener, reverse flattener,
and +100 bp 7-year local shock. No carry, roll or elapsed-time cash flows. Compare exact P&L,
bucket first-order estimate and parallel second-order approximation where appropriate.
Report unhedged and hedged residuals; a parallel-neutral hedge cannot remove every shape risk.

Controlled alternatives: log-linear discount vs linear-zero interpolation, bond Actual/360 vs
ISMA with identical schedule/coupon, and single vs dual projection. Reconcile calibration before
interpreting price differences. These are model/convention effects, not bid/ask discrepancies.

FX case: USD per EUR, spot 1.10, one-year date from reference, domestic USD curve and illustrative
EUR flat continuous 2.5% (Actual/365F), zero cross-currency basis and compatible collateral
assumed. Forward F=S D_EUR/D_USD. A long EUR forward has USD PV=S D_EUR-K D_USD. Check zero
PV at K=F and opposite signs off-market; this is conditional CIP, not executable arbitrage.

Recovery: `uv run python research/run_study.py` completes in seconds from versioned illustrative
fixtures; no download. Results/figures and executed study are replaceable; original notebooks,
spreadsheets and screenshots are preserved on old and in ignored local recovery. Legacy options,
FRA, cross-currency swaps and CDS are not claimed validated extensions.

Implementation convention made explicit during independent reconciliation: use indexed Ibor coupons in both term-curve helpers and the valued swap. Forward rates use index value/maturity dates and index accrual, then scale by the actual coupon accrual; holiday-adjusted schedules can make those periods differ. The par-coupon approximation is not silently mixed with indexed coupons.

## Teaching collection supplement — 19 September 2026

Eleven maintained topic chapters now introduce the original product areas. Their standalone
notebooks use the core fixture or explicitly stated additional illustrative assumptions.
They do not change the primary bond/swap hedge hypothesis, inputs, scenarios or acceptance
tolerances above. BSM adds formula/engine/parity checks; FRA uses deterministic settlement;
cross-currency swaps use fixed-for-fixed par legs with zero basis; CDS uses continuous premiums
and constant hazard. The latter examples are analytical teaching cases, not full contract or
market validation. See [topic overview](../README.md) and each chapter's stated limits.
