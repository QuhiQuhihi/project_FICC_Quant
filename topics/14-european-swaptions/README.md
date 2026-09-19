# European swaptions and annuity pricing

Construct a forward swap and price the right to pay or receive fixed using its discounted annuity.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A payer swaption gives the right to enter a payer swap at a fixed coupon; a receiver swaption gives the opposite right. Its underlying is a forward-starting swap, so the option price depends on the forward par rate and the discounted fixed-leg annuity, not on one bond yield.

The example uses one-year European exercise into a five-year USD swap with annual fixed and quarterly synthetic term-floating payments. Notional is 100, accrual is Actual/360, dates are Modified Following, fixing lag is zero, and the core illustrative projection and OIS discount curves remain distinct. `VanillaSwap`, `EuropeanExercise`, `Swaption` and `BlackSwaptionEngine` make the full contract-to-engine path visible. Settlement is physical; there is no cash-annuity convention to infer.

For annuity $A=N\sum_i\alpha_iD_i$, forward swap rate $F$, strike $K$ and expiry $T$, the payer price is $A[F\Phi(d_1)-K\Phi(d_2)]$, with $d_1=\log(F/K)/(\sigma\sqrt T)+\sigma\sqrt T/2$. The notebook reconstructs the annuity from fixed coupons, checks the forward swap PV against $A(F-K)$, compares QuantLib to a direct Black calculation, and verifies payer–receiver parity at three strikes. A quote update reprices the same at-the-money contract at several volatilities.

The 20% input is a flat lognormal swap-rate volatility, not 20 basis points of normal volatility. Positive rates are required by this unshifted Black example. No smile, volatility-surface calibration, Bermudan exercise or dynamic hedging is claimed. See [QuantLib swaption engines](https://quantlib-python-docs.readthedocs.io/en/latest/pricing_engines/swaptions.html) and the [Black engine implementation](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/swaption/blackswaptionengine.hpp).

## What to take away

The discounted annuity and forward rate reproduce QuantLib's European price. Payer–receiver parity equals the forward swap value, and volatility quote changes propagate to the same option contract.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
