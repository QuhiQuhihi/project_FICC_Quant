# Quotes, handles and scenario risk

Update a market quote, relink a curve and revalue the same bond without rebuilding its contract.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A trader changes a rate and expects every dependent instrument to update. QuantLib's observable quotes and handles connect that workflow: `SimpleQuote` supplies a rate, `FlatForward` observes it, `RelinkableYieldTermStructureHandle` identifies the curve, and `DiscountingBondEngine` values the contract.

The example fixes a two-year zero-coupon bond, face 100 and zero settlement days. Its flat continuously compounded rate starts at 3.5% with Actual/365 Fixed. Quote shocks change the same live bond's value. The notebook compares each result against $100e^{-rT}$, checks signed zero-rate DV01 against $-T PV\times10^{-4}$, restores the quote after the sweep, and relinks the handle to an independently created 4.5% curve before restoring the original link.

The scenario object is the continuously compounded flat zero rate, not an OIS market-quote strip. That distinction determines what the reported sensitivity means. The [bond-risk chapter](../05-bond-risk/README.md) supplies quote-bucket risk with complete curve rebuilds. Fixed reference dates make these instantaneous scenarios: no carry, roll-down or settlement-date movement is included.

Both quote restoration and handle restoration are checked. This is useful for avoiding one scenario contaminating the next, but it does not model a production market-data feed. See [QuantLib handles](https://github.com/lballabio/QuantLib/blob/master/ql/handle.hpp) and [simple quotes](https://github.com/lballabio/QuantLib/blob/master/ql/quotes/simplequote.hpp).

## What to take away

Quote updates and curve relinking both propagate to the existing instrument. Every scenario matches direct discounting, the finite-difference sensitivity matches the derivative, and the original quote and link are restored.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
