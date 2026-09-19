# Project FICC Quant

How do cash-flow design, market conventions and model assumptions determine a financial instrument's price and risk? This research collection connects options, rates, foreign exchange and credit through that question. Each topic starts with the economic contract, develops an explicit valuation argument and ends with a numerical example that readers can inspect in its notebook.

The central thread is **from a curve to a price, from a price to risk, and from risk to a hedge**. A connected bond-and-swap study follows that thread in depth. The shorter topic chapters let readers explore individual products and see where the same ideas carry across markets.

## Explore the research

| Topic | What the chapter investigates | Details and calculations |
|---|---|---|
| Black–Scholes–Merton options | How volatility, moneyness and dividends shape European option values. | [Read](topics/01-bsm-options/README.md) · [Notebook](topics/01-bsm-options/study.ipynb) |
| Yield curves and discount factors | Turn par quotes into dated discount factors and forward rates. | [Read](topics/02-yield-curves/README.md) · [Notebook](topics/02-yield-curves/study.ipynb) |
| Yield-curve inversion | Separate a negative term spread from a recession forecast. | [Read](topics/03-curve-inversion/README.md) · [Notebook](topics/03-curve-inversion/study.ipynb) |
| Bond valuation and accrued interest | Trace a bond price to coupons, principal, day counts and discounting. | [Read](topics/04-bond-valuation/README.md) · [Notebook](topics/04-bond-valuation/study.ipynb) |
| Bond Greeks, curve risk and hedging | See what duration removes, what convexity adds and what a one-swap hedge leaves. | [Read](topics/05-bond-risk/README.md) · [Notebook](topics/05-bond-risk/study.ipynb) |
| Swap curves: projection and discounting | Separate the curve forecasting floating coupons from the curve discounting payments. | [Read](topics/06-swap-curves/README.md) · [Notebook](topics/06-swap-curves/study.ipynb) |
| Forward rate agreements | Connect a forward borrowing rate to the sign and settlement of an FRA. | [Read](topics/07-forward-rate-agreements/README.md) · [Notebook](topics/07-forward-rate-agreements/study.ipynb) |
| Interest rate swaps | Build a fixed-for-floating swap from its two legs and freeze it before hedging. | [Read](topics/08-interest-rate-swaps/README.md) · [Notebook](topics/08-interest-rate-swaps/study.ipynb) |
| FX forwards and covered interest parity | Price a future currency exchange with dated domestic and foreign cash flows. | [Read](topics/09-fx-forwards/README.md) · [Notebook](topics/09-fx-forwards/study.ipynb) |
| Cross-currency swaps | Track principal exchanges, coupon legs and the currency used to report value. | [Read](topics/10-cross-currency-swaps/README.md) · [Notebook](topics/10-cross-currency-swaps/study.ipynb) |
| Credit default swaps | Relate survival, recovery and protection payments to the premium leg. | [Read](topics/11-credit-default-swaps/README.md) · [Notebook](topics/11-credit-default-swaps/study.ipynb) |

For a first pass, follow **yield curves → bond valuation → bond risk → interest rate swaps**. For currency funding, start with **FX forwards → cross-currency swaps**. Options and CDS offer two different extensions: nonlinear market exposure and contingent default payments.

## The connected study: how much does one swap hedge?

The main experiment values a synthetic 4% bond and a seven-year payer swap with separate projection and discount curves. It first reconciles calibration and cash flows, then freezes the hedge and shocks parallel rates, curve slope and a local maturity. This exposes the distinction between neutralizing one sensitivity and controlling the complete shape of a curve.

<!-- STUDY_RESULT_START -->
Under the explicit illustrative inputs, a bond priced at **103.195569 per 100** is parallel-DV01-neutralized with **1.009745 units** of a payer swap (each unit has notional 100). The largest absolute residual among five frozen instantaneous scenarios is **0.071261 per 100**, in **local_7y**. A single parallel hedge leaves curve-shape and convexity risk.
<!-- STUDY_RESULT_END -->

![Frozen hedge residuals under illustrative curve shocks](research/figures/hedge.png)

[Read the study design](docs/01-methods.md) · [Explore the results](docs/02-results.md) · [Open the full executed notebook](study.ipynb)

## What the examples establish

All rates and product inputs are explicitly constructed assumptions. The core study establishes numerical calibration, independent cash-flow reconciliation and the effects of controlled convention changes. The topic chapters add analytical checks such as option parity, FRA settlement direction, currency cash-flow balance and CDS premium/protection equality.

These examples do not claim live market calibration or executable trading opportunities. In particular, the cross-currency chapter is a fixed-for-fixed cash-flow example and the CDS chapter uses continuous premiums; their limits are explained where the calculations appear. Original topic notebooks remain available in the preserved `old` branch, while the linked chapters are the maintained research collection.

[Sources and provenance](research/SOURCES.md) · [Research protocol](research/PROTOCOL.md) · [Further research](research/RESEARCH_AGENDA.md) · [Reproduction details](docs/reproduction.md)
