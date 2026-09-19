# Swap curves: projection and discounting

Separate the curve forecasting floating coupons from the curve discounting payments.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A floating coupon forecast and the present value of that coupon serve different roles. This chapter asks what changes when a term-index projection curve is distinct from the collateral discount curve.

For a synthetic term index, the projected simple rate is $L=[P^{proj}(t_a)/P^{proj}(t_b)-1]/\tau_{index}$. The coupon amount uses its actual contract accrual and is discounted with $D^{disc}(t_{pay})$. Index value/maturity dates can differ slightly from coupon accrual dates after holiday adjustments.

The fixture supplies OIS par quotes and an illustrative term swap strip 50 basis points above it. QuantLib first bootstraps the OIS discount curve, then builds the term projection curve while discounting its calibration helpers with OIS. The notebook checks both sets of helper residuals and values the same payer swap using dual curves and an OIS-only projection counterfactual. Its fixed coupon remains frozen across that comparison.

The synthetic USD 3M index is not current USD LIBOR. A constant 50-bp input difference is a teaching assumption, not a statement about observed credit or basis premia. The study does not calibrate a full collection of overnight, term, futures, basis and collateral instruments.

Calibration error measures the reproduction of input quotes. The single-curve valuation difference measures a controlled modeling choice. Neither is an observed market pricing error. See [IRS cash flows](../08-interest-rate-swaps/README.md) for the coupon-level reconciliation.

## What to take away

Both curves reproduce their own calibration instruments. Substituting the discount curve for term projection changes the swap PV while its contractual fixed coupon remains unchanged.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
