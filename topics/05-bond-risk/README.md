# Bond Greeks, curve risk and hedging

See what duration removes, what convexity adds and what a one-swap hedge leaves.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

“DV01” is incomplete without the variable that moves. A parallel yield bump, a continuous zero spread and a parallel shift to bootstrapped market quotes can produce different sensitivities because they change different objects.

The connected study defines signed quote DV01 as $[P(q+1bp)-P(q-1bp)]/2$, in currency per positive basis point. It rebuilds discount and projection curves for each bump. Bond DV01 is negative with this convention. Separate quote buckets reveal the term-structure directions hidden in one parallel number.

The notebook independently differentiates discounted bond cash flows with respect to a continuous zero spread: $-10^{-4}\sum_i t_iCF_iD_i$. A central difference checks that derivative. It then reads the primary study's frozen hedge and scenario revaluations, verifying $\Delta P_{hedged}=\Delta P_{bond}+h\Delta P_{swap}$. The companion figure compares exact residuals with a bucket approximation across parallel, slope and local-tenor shocks.

The hedge ratio $h=-DV01_{bond}/DV01_{swap}$ removes one first-order direction at inception. It does not cancel every tenor bucket, the separate projection exposure, or all second-order effects. All shocks are instantaneous, with coupon and positions frozen. Carry, roll-down, trade costs and rebalancing are outside this experiment.

[The full study](../../study.ipynb) retains the calibrated inputs, bump-size checks and convention alternatives needed to interpret these residuals.

## What to take away

The independent zero-spread derivative agrees with its finite difference. The frozen swap removes most parallel sensitivity, while the local 7Y and slope shocks expose residual curve risk. Zero-spread DV01 and quote DV01 remain different measures.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
