# Yield curves and discount factors

Turn par quotes into dated discount factors and forward rates.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A quoted par rate, a zero rate and a forward rate answer different questions. A par rate makes a specified coupon instrument worth par; a discount factor prices one unit paid at a future date; a forward rate prices the exchange between two future dates.

For continuously compounded zero rates, $D(0,t)=e^{-z(t)t}$. With a declared simple accrual $\tau$, the discount-implied forward is $F(t_1,t_2)=[D(0,t_1)/D(0,t_2)-1]/\tau$. These transformations must use compatible dates and day counts.

This chapter bootstraps the versioned 1–10-year illustrative OIS par strip using explicit calendar and coupon conventions. It displays input quotes beside the zero and forward rates produced by the curve. Each helper must reprice its input within $10^{-8}$ in decimal rate units. The plot makes clear why a par quote should not be inserted directly as a zero rate.

The curve uses log-linear discount interpolation and Actual/365 Fixed zero-rate reporting. The forward-rate table uses Actual/360 accruals between adjusted annual dates. Only maturities covered by the fixture are used. Positive discount factors are required; monotonic decline is not imposed as a universal condition because negative-rate environments can imply discount factors above one.

These are constructed rates dated 15 September 2026. This chapter studies internal curve consistency; no daily Treasury series, live SOFR term surface or executable quote set is being reproduced. See the [core conventions](../../docs/01-methods.md) for the exact instrument definitions.

## What to take away

The same calibrated curve produces distinct par, zero and forward rates. Small repricing errors establish consistency with the declared inputs, not the accuracy of those inputs as market observations.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
