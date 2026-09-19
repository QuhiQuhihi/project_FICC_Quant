# Bond valuation and accrued interest

Trace a bond price to coupons, principal, day counts and discounting.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A bond price becomes inspectable when every remaining payment has a date, amount and discount factor. The dirty price is the present value of those payments; the clean price removes accrued interest under the contract's accrual convention.

$$P_{dirty}=\sum_i CF_iD(0,t_i),\qquad P_{clean}=P_{dirty}-AI.$$

The case is a synthetic USD 100-face bond paying 4% annually in semiannual installments, issued in March 2026 and maturing in September 2033. The primary day count is Actual/Actual ISMA. The notebook reconstructs the dated cash flows independently and reconciles their discounted sum with QuantLib at 15 September 2026. A second valuation one month later uses a newly anchored flat 3.5% curve solely to expose nonzero accrued interest and verify the clean/dirty identity.

The second date is a separate convention exercise, not a holding-period P&L or a forecast of curve evolution. On each date, past/reference-date payments are excluded consistently. Zero settlement days keeps the independent PV and the engine on the same date; production settlement rules require corresponding treatment.

There is no credit, liquidity, tax or embedded-option spread. The price is therefore conditional on the supplied discount curve and synthetic contract, not a valuation of a quoted Treasury CUSIP or corporate bond. The risk chapter builds on the same cash-flow view to distinguish a yield derivative from a rebuilt-curve quote sensitivity.

## What to take away

The cash-flow sum matches the engine. Accrued interest is zero on the primary coupon date and positive in the separate October convention example; clean and dirty prices reconcile on both dates.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
