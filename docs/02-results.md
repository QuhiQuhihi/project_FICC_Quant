# Curves, conventions and the limits of a one-swap hedge

Under the explicit illustrative inputs, a bond priced at **103.195569 per 100** is parallel-DV01-neutralized with **1.009745 units** of a payer swap (each unit has notional 100). The largest absolute residual among five frozen instantaneous scenarios is **0.071261 per 100**, in **local_7y**. A single parallel hedge leaves curve-shape and convexity risk.

These are numerical model results from constructed quotes dated 15 September 2026. No residual is an observed mispricing or executable trading opportunity.

## Independent valuation and calibration

| instrument | quantlib_pv | independent_pv | residual | clean | accrued | dirty |
| --- | --- | --- | --- | --- | --- | --- |
| bond | 103.196 | 103.196 | 2.84217e-14 | 103.196 | 0 | 103.196 |
| payer_swap | -3.55271e-14 | -2.77556e-15 | -3.27516e-14 | — | — | — |

Maximum quote repricing error is 3.88e-14 in decimal rate units; maximum independent cash-flow PV discrepancy is 3.28e-14 currency. Internal calibration accuracy is separate from market accuracy.

## Controlled assumptions

| case | bond_pv | swap_pv | bond_difference | swap_difference |
| --- | --- | --- | --- | --- |
| dual_logdiscount | 103.196 | -3.55271e-14 | 0 | 0 |
| single_curve | 103.196 | -3.09294 | 0 | -3.09294 |
| linear_zero | 103.194 | 0.000278217 | -0.00153874 | 0.000278217 |
| bond_act360 | 103.556 | -3.55271e-14 | 0.360369 | 0 |

The term swap uses separate projection and discounting. Replacing its projection with OIS changes floating cash flows while the fixed coupon stays frozen. The bond day-count comparison changes coupon accrual; interpolation changes off-node values even when instruments calibrate.

## Frozen hedge scenarios

| scenario | unhedged_bond_pnl | swap_pnl_per100 | hedged_pnl | bucket_first_order | parallel_second_order |
| --- | --- | --- | --- | --- | --- |
| parallel_up100 | -6.01785 | 5.95846 | -0.00133028 | -7.0773e-08 | -0.00138919 |
| parallel_down100 | 6.48771 | -6.42654 | -0.00145169 | 7.0773e-08 | -0.00138919 |
| steepener | -1.01685 | 1.0375 | 0.0307564 | 0.0306816 | — |
| flattener | 1.01309 | -1.03363 | -0.0306081 | -0.0306816 | — |
| local_7y | -6.09793 | 6.10966 | 0.0712615 | 0.0724131 | — |

Quote buckets are rebuilt-curve sensitivities, not zero-rate or yield-duration bumps. The bucket approximation is first order; the parallel second-order column is defined only for parallel shocks. Positions are held fixed, with no elapsed-time carry or cash flows.

![Hedge residuals](../research/figures/hedge.png)

## FX consistency

With USD per EUR spot 1.10, the one-year illustrative fair forward is **1.114175 USD/EUR**. Its discounted cash-flow PV is zero to numerical tolerance under zero-basis, compatible-collateral assumptions. This verifies signs and parity, not executable cross-currency arbitrage.

The core is validated numerically. Live collateral, fixing, instrument and quote evidence is still required for a market study. Legacy options, CDS and cross-currency examples remain explicitly unvalidated archival context. See [conventions and methods](01-methods.md), [protocol](../research/PROTOCOL.md), [source register](../research/SOURCES.md), and [unrun extensions](../research/RESEARCH_AGENDA.md).
