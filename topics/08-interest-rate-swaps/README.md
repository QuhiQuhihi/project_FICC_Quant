# Interest rate swaps

Build a fixed-for-floating swap from its two legs and freeze it before hedging.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A payer interest rate swap exchanges fixed payments for floating receipts. The fair fixed coupon sets their initial present values equal; it is a property of the schedule, projection and discounting assumptions together.

Writing the fixed annuity as $A=\sum_i\alpha_iD_i$ and the projected floating value per unit notional as $B$, the fair rate is $K^*=B/A$. A swap with a frozen coupon $K$ has $PV=N(B-KA)$ from the payer's perspective.

The case starts one business day after 15 September 2026, lasts seven years, pays fixed annually and receives a synthetic USD 3M rate quarterly. It uses Actual/360, Modified Following and separate term projection/OIS discount curves. The next-business-day start avoids a hidden requirement for historical index fixings.

The notebook reconstructs each leg from indexed-coupon dates, computes the fair rate independently and compares the total PV with QuantLib. It then raises the fixed coupon by 10 bp and checks the analytical annuity effect. This holds the forecast curve and floating leg fixed, separating a contractual coupon change from a market-curve shock.

There is no principal exchange in this single-currency IRS. The seven-year payer becomes the hedge instrument in the connected bond study. When scenarios move curves, its coupon and hedge units stay frozen; recalculating a fair coupon after each shock would replace the original contract and erase the risk being studied.

## What to take away

Independent floating cash flows and the fixed annuity reproduce the fair coupon. Paying an additional 10 bp reduces PV by exactly notional times the annuity times 0.001 under unchanged curves.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
