# CDS hazard calibration and credit legs

Bootstrap survival from a spread strip, price a quarterly CDS, and reconcile premium and protection legs.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A credit desk needs more than the approximation spread ≈ loss-given-default × hazard. A CDS curve must reproduce quoted contracts under declared premium, default and settlement conventions.

This notebook constructs illustrative 1Y, 3Y and 5Y spreads of 80, 110 and 140 bp with recovery 40%, then uses `SpreadCdsHelper` and `PiecewiseFlatHazardRate`. The discount curve is the collection's OIS fixture. Helpers use zero settlement days, quarterly premiums, Following, Forward schedule generation and Actual/360. Helper implied quotes must match the input strip within $10^{-8}$ decimal rate units. Survival must remain between zero and one and decrease with maturity.

Next, `CreditDefaultSwap` and `MidPointCdsEngine` value a separate five-year protection-buyer ticket with running premium 100 bp, notional 100, protection starting on the reference date, quarterly Forward schedule, Actual/360, premium accrued on default, payment at default, no accrual rebate and zero cash-settlement days. It is intentionally an off-market ticket, not an assertion that its conventions equal every calibration-helper convention. The notebook independently sums survival-weighted premiums, accrued premium at midpoint default and loss-given-default payments; it then reprices the ticket at its own fair spread.

Midpoint default integration is a numerical approximation. This example is not an ISDA Standard Model validation and uses neither standard IMM contracts nor observed credit quotes. Hazard is a pricing-measure input, not a physical default forecast. References: [QuantLib Python CDS example](https://github.com/lballabio/QuantLib-SWIG/blob/master/Python/examples/cds.py), [midpoint engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/credit/midpointcdsengine.cpp), and [ISDA model](https://www.cdsmodel.com/).

## What to take away

The spread helpers reprice, survival is valid, and independently summed midpoint cash flows reproduce QuantLib's two legs and total PV. The ticket's fair spread belongs to its stated contract conventions; it is not automatically the five-year helper quote.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
