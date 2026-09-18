# From curve quotes to frozen hedge P&L

A yield curve is a mapping from dated cash flows to present value, not just a line through
rates. Deposits, par swaps, zero rates and discount factors encode different objects. This
study begins with explicit constructed par quotes and asks which price/risk differences arise
when assumptions change.

## Contract and convention table

| Item | Primary numerical assumption |
|---|---|
| Valuation | 15 September 2026; no elapsed time in scenarios |
| Currency/notional | USD; 100 bond face and 100 per swap unit |
| Calendar/adjustment | US GovernmentBond; Modified Following |
| Settlement | Zero days for aligned independent PV comparisons |
| Discount inputs | 1–10Y illustrative SOFR-style OIS par quotes; annual fixed, Actual/360 |
| Discount interpolation | Log-linear discount factors; no required extrapolation |
| Projection | Synthetic USD 3M term index; zero fixing lag; Actual/360 |
| Swap | Forward-start one business day; 7Y payer; annual fixed, quarterly floating |
| Floating coupons | Indexed coupons, explicit index value/maturity dates |
| Bond | 4% coupon; semiannual; Actual/Actual ISMA; March 2026–September 2033 |
| Bond spread | Zero credit/liquidity spread, an illustration rather than a Treasury CUSIP |
| FX | USD per EUR; spot 1.10; EUR flat continuous 2.5%; zero basis assumed |

The synthetic term index is not a surviving USD LIBOR contract. SOFR's overnight reference
rate is not a complete OIS quote strip. The fixture has no claim to matching live quotes,
CSA terms, benchmark fixings or executable collateralized funding.

## Calibration and independent valuation

QuantLib bootstraps each instrument to its quoted par rate. Projection helpers discount
using the separate OIS curve. Repricing errors must remain below 1e-8 in decimal rate units.
This verifies internal consistency, not the correctness of unobserved market inputs.

The bond's independent PV sums coupon/principal amounts times discount factors. The payer
swap adds floating coupons and subtracts fixed coupons. Each floating rate comes from the
projection ratio (P(value)/P(maturity)-1)/index_accrual and is multiplied by the coupon's
actual accrual before discounting. Holiday adjustments can make those periods differ;
using an implicit par-coupon approximation in one calculation and indexed coupons in another
creates a small genuine convention difference. Both calculations now use indexed coupons.

## Risk has an object and a unit

Signed quote DV01 is [PV(q+1bp)-PV(q-1bp)]/2: currency per positive basis point, with curves
rebuilt. For a fixed-rate bond it is negative. Quote buckets separately perturb discount and
projection pillars. This differs from a yield bump and from a parallel continuous zero spread.
For the latter, an independent derivative is -sum(t CF D) times 1e-4. Bumps of .1, 1 and 5 bp
check finite-difference stability; second differences quantify curvature in currency/bp squared.

## Hedging is a local statement

Hold h=-bond_DV01/swap_DV01 swap units. Freeze h and the swap coupon before every scenario.
Parallel neutrality removes one first-order direction; it does not neutralize a full vector
of quote risks. Large shocks also expose convexity. The scenario table reports exact
revaluation, quote-bucket first order, and a second-order parallel approximation. None includes
carry, roll-down or intervening cash flows.

FX parity follows from matching dated currency cash flows: F=S D_EUR/D_USD; long-EUR forward
PV in USD is S D_EUR-K D_USD. The fair strike has zero PV under the declared no-basis assumptions.
An executable transaction needs observed bid/ask, collateral, funding and settlement terms.

[Generated valuation and hedge evidence](02-results.md) · [Full protocol and tolerances](../research/PROTOCOL.md).
