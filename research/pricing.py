"""Explicit illustrative curves, cash flows, and signed quote risk."""

from contextlib import contextmanager
import json
import numpy as np
import pandas as pd
import QuantLib as ql
from research.common import ROOT, sha

DATE = ql.Date(15, 9, 2026)
CAL = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
DC = ql.Actual360()
NOTIONAL = 100.0


@contextmanager
def valuation_date(date=DATE):
    settings = ql.Settings.instance()
    old = settings.evaluationDate
    settings.evaluationDate = date
    try:
        yield
    finally:
        settings.evaluationDate = old


def fixture():
    manifest = json.loads((ROOT / "research/data/input_manifest.json").read_text())
    source = manifest["inputs"][0]
    path = ROOT / source["path"]
    if sha(path) != source["sha256"]:
        raise ValueError("Illustrative input changed: document a new fixture version")
    return pd.read_csv(path)


def index(handle=ql.YieldTermStructureHandle()):
    return ql.IborIndex(
        "Illustrative USD 3M",
        ql.Period(3, ql.Months),
        0,
        ql.USDCurrency(),
        CAL,
        ql.ModifiedFollowing,
        False,
        DC,
        handle,
    )


def curves(quotes=None, interpolation="log_discount"):
    q = fixture() if quotes is None else quotes
    constructor = (
        ql.PiecewiseLogLinearDiscount if interpolation == "log_discount" else ql.PiecewiseLinearZero
    )
    ois = [
        ql.OISRateHelper(
            0,
            ql.Period(int(row.years), ql.Years),
            float(row.ois_rate),
            ql.Sofr(),
            paymentConvention=ql.ModifiedFollowing,
            paymentCalendar=CAL,
        )
        for row in q.itertuples()
    ]
    discount = constructor(DATE, ois, ql.Actual365Fixed())
    discount.discount(discount.maxDate())
    dh = ql.YieldTermStructureHandle(discount)
    helpers = [
        ql.SwapRateHelper(
            float(row.term_rate),
            ql.Period(int(row.years), ql.Years),
            CAL,
            ql.Annual,
            ql.ModifiedFollowing,
            DC,
            index(),
            ql.QuoteHandle(),
            ql.Period(0, ql.Days),
            dh,
            0,
            ql.Pillar.LastRelevantDate,
            ql.Date(),
            False,
            True,
        )
        for row in q.itertuples()
    ]
    projection = constructor(DATE, helpers, ql.Actual365Fixed())
    projection.discount(projection.maxDate())
    residuals = []
    for kind, hs, column in [("discount", ois, "ois_rate"), ("projection", helpers, "term_rate")]:
        for h, (_, row) in zip(hs, q.iterrows()):
            residuals.append(
                {
                    "curve": kind,
                    "years": row.years,
                    "quote": row[column],
                    "implied": h.impliedQuote(),
                    "residual": h.impliedQuote() - row[column],
                    "pillar": h.pillarDate().ISO(),
                }
            )
    return discount, projection, pd.DataFrame(residuals)


def schedule(start, end, period):
    return ql.Schedule(
        start,
        end,
        period,
        CAL,
        ql.ModifiedFollowing,
        ql.ModifiedFollowing,
        ql.DateGeneration.Backward,
        False,
    )


def bond(discount, day_count=None):
    dc = ql.ActualActual(ql.ActualActual.ISMA) if day_count is None else day_count
    dates = schedule(ql.Date(15, 3, 2026), ql.Date(15, 9, 2033), ql.Period(6, ql.Months))
    b = ql.FixedRateBond(0, NOTIONAL, dates, [0.04], dc, ql.ModifiedFollowing)
    b.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(discount)))
    rows = []
    for i in range(1, len(dates)):
        if dates[i] <= DATE:
            continue
        tau = dc.yearFraction(dates[i - 1], dates[i], dates[i - 1], dates[i])
        amount = NOTIONAL * 0.04 * tau + (NOTIONAL if i == len(dates) - 1 else 0)
        rows.append(
            {
                "instrument": "bond",
                "date": dates[i].ISO(),
                "accrual": tau,
                "amount": amount,
                "discount": discount.discount(dates[i]),
                "pv": amount * discount.discount(dates[i]),
            }
        )
    return b, pd.DataFrame(rows)


def swap(discount, projection, coupon=None):
    start = CAL.advance(DATE, 1, ql.Days)
    end = start + ql.Period(7, ql.Years)
    fixed = schedule(start, end, ql.Period(1, ql.Years))
    floating = schedule(start, end, ql.Period(3, ql.Months))
    idx = index(ql.YieldTermStructureHandle(projection))

    def build(rate):
        s = ql.VanillaSwap(
            ql.VanillaSwap.Payer,
            NOTIONAL,
            fixed,
            rate,
            DC,
            floating,
            idx,
            0.0,
            DC,
            ql.ModifiedFollowing,
            True,
        )
        s.setPricingEngine(ql.DiscountingSwapEngine(ql.YieldTermStructureHandle(discount)))
        return s

    preliminary = build(0.04)
    rate = preliminary.fairRate() if coupon is None else coupon
    s = build(rate)
    rows = []
    for leg, dates in [("fixed", fixed), ("float", floating)]:
        for a, b in zip(list(dates)[:-1], list(dates)[1:]):
            tau = DC.yearFraction(a, b)
            if leg == "fixed":
                amount = -NOTIONAL * rate * tau
            else:
                value = idx.valueDate(idx.fixingDate(a))
                maturity = idx.maturityDate(value)
                forward = (
                    projection.discount(value) / projection.discount(maturity) - 1
                ) / DC.yearFraction(value, maturity)
                amount = NOTIONAL * forward * tau
            rows.append(
                {
                    "instrument": leg,
                    "date": b.ISO(),
                    "accrual": tau,
                    "amount": amount,
                    "discount": discount.discount(b),
                    "pv": amount * discount.discount(b),
                }
            )
    return s, pd.DataFrame(rows), rate


def value(quotes, coupon, interpolation="log_discount", single=False, bond_dc=None):
    d, p, _ = curves(quotes, interpolation)
    b, _ = bond(d, bond_dc)
    s, _, _ = swap(d, d if single else p, coupon)
    return np.array([b.NPV(), s.NPV()])


def bumped(quotes, ois=None, term=None):
    q = quotes.copy()
    if ois is not None:
        q["ois_rate"] += np.asarray(ois)
    if term is not None:
        q["term_rate"] += np.asarray(term)
    return q


def quote_risk(quotes, coupon, bump_bps=1.0):
    h = bump_bps * 1e-4
    up = value(bumped(quotes, h, h), coupon)
    down = value(bumped(quotes, -h, -h), coupon)
    base = value(quotes, coupon)
    return (up - down) / (2 * bump_bps), (up - 2 * base + down) / bump_bps**2


def fx_forward(spot, domestic, foreign):
    if min(spot, domestic, foreign) <= 0:
        raise ValueError("Spot and discount factors must be positive")
    return spot * foreign / domestic
