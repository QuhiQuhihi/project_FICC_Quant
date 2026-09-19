# Cross-currency swaps

Track principal exchanges, coupon legs and the currency used to report value.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A cross-currency swap exchanges cash flows in two currencies. The principal exchanges matter alongside the coupons: dropping them changes the exposure being valued.

This deliberately simple case is a five-year, fixed-for-fixed swap. At inception the holder receives EUR 100 and pays USD 110 at spot 1.10 USD/EUR. During the swap the holder pays EUR coupons and receives USD coupons; at maturity the holder returns EUR 100 and receives USD 110. Each currency's coupon is set to its own par fixed-bond rate under the declared flat curve.

For currency $c$, annual accruals and discount factors $D_c(i)$ give $k_c=[1-D_c(T)]/\sum_iD_c(i)$. The remaining-leg USD value immediately after inception is $PV_{USD\ leg}-S\,PV_{EUR\ leg}$. At par inception both legs and the initial exchanges cancel. After inception, moving the conversion spot while holding the contractual coupons and curves fixed exposes the position's FX sensitivity.

The notebook explicitly lists the time-zero and final principal exchanges, checks par leg values, and compares a finite-difference spot derivative with $-PV_{EUR\ leg}$. A separate 10-bp change to the contractual EUR coupon shows the coupon-annuity effect; it is not a calibrated market basis spread.

Assumptions are flat continuous USD 4% and EUR 2.5%, deterministic rates, annual exact-year payments, zero basis and compatible collateral. This is neither a floating-versus-floating basis-swap engine nor a collateralized multi-currency curve bootstrap. Resettable notionals, currency-specific calendars, funding, collateral and observed basis quotes remain outside this chapter. [BIS](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis) provides the institutional context for that boundary.

## What to take away

The two par legs and the initial principal exchange balance at inception. The remaining fixed cash flows still carry FX exposure; a zero initial value does not imply a risk-free position. No market currency basis is estimated.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
