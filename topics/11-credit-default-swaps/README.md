# Credit default swaps

Relate survival, recovery and protection payments to the premium leg.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A CDS protection buyer pays premiums while a reference entity survives and receives compensation after a covered default. Pricing requires both the survival distribution and the loss given default; a credit spread alone does not uniquely identify default probability without further assumptions.

This chapter uses a continuous-premium approximation with constant risk-neutral hazard $\lambda$, recovery $R$ and discount rate $r$. Survival is $Q(t)=e^{-\lambda t}$. The risky premium annuity is $A=\int_0^T e^{-(r+\lambda)t}dt$ and the protection value per unit notional is $(1-R)\lambda A$. The fair continuous spread is therefore $s^*=(1-R)\lambda$.

At $T=5$, $r=3.5\%$, $\lambda=2\%$ and $R=40\%$, numerical quadrature independently checks the analytical annuity. The notebook compares premium and protection values, plots fair spreads across hazard/recovery assumptions, and verifies that the fair contract has zero PV. The probabilities are model assumptions under a pricing measure, not estimated frequencies or default forecasts.

Continuous premiums avoid the quarterly coupon schedule and accrued premium at default that a standard contract needs. The example omits upfront payments, settlement delays, restructuring/documentation terms and calibration to a spread term structure. It is an analytical teaching case, not an implementation or validation of the ISDA Standard Model.

For standard contract pricing and consistent conversion between upfront amounts and quoted spreads, the primary reference is the [ISDA CDS Standard Model](https://www.cdsmodel.com/). A credible market extension would compare an implementation against its test grids using fully specified dates, recovery and input curves.

## What to take away

The fair continuous premium is 120 bp/year for the declared 2% hazard and 40% recovery. Different recovery assumptions map the same hazard to different spreads; this does not calibrate a standard quarterly CDS.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
