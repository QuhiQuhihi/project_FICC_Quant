# Forward rate agreements in QuantLib

Construct a receive-floating FRA, separate projection from discounting, and reconcile start settlement.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A desk FRA locks the rate for one future borrowing period. Here the long position receives floating and pays fixed on notional 100. It starts six months after 15 September 2026 and ends three index months later. The synthetic USD 3M index has zero fixing lag, Modified Following dates and Actual/360 accrual; it is not a live traded benchmark.

The notebook builds `IborIndex`, two `YieldTermStructureHandle` objects and `ForwardRateAgreement`. The index supplies projection; a separate handle supplies OIS discounting. The explicit-maturity constructor uses a discount-ratio forward. Choosing the end date from `index.maturityDate(start)` keeps this example aligned with the index period.

For the projected rate $L$, strike $K$ and accrual $\tau$, start settlement is $N\tau(L-K)/(1+\tau L)$. We reconstruct this amount and its discounted PV independently, check buyer/seller symmetry, and compare strikes 50 bp below, at and above the forward. QuantLib's constructor order is checked against the installed locked version; older Python examples can use a different order.

This is the library's deterministic forward substitution, not a stochastic settlement-convexity model. All fixings are future dates, so no historical fixing is silently supplied. A production ticket also needs its actual index, fixing availability, broken-date treatment and legal settlement convention. See the [QuantLib FRA implementation](https://github.com/lballabio/QuantLib/blob/master/ql/instruments/forwardrateagreement.cpp).

## What to take away

QuantLib agrees with independently calculated start settlement and discounted PV. The at-forward FRA is zero; reversing the position reverses value. Projection and discounting remain separate inputs.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
