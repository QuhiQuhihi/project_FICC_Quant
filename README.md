# QuantLib for the FICC desk

A hands-on collection of **QuantLib implementations for fixed income, currencies and credit**. The aim is to connect a desk question to a dated instrument, its cash flows, a pricing engine and an interpretable risk measure. Each chapter pairs concise research notes with an executed notebook whose inputs, QuantLib objects and numerical checks are visible.

Start with a workflow that interests you: build a curve, value a bond, hedge a rate exposure, cap a floating payment or calibrate credit survival. The examples show how calendars, accrual rules, fixing dates, projection curves, discount curves and volatility assumptions enter the calculation. All quotes are explicit illustrative inputs, so the notebooks can be explored without a vendor terminal.

## Explore the desk examples

| Desk question | What you build or investigate | Open the chapter |
|---|---|---|
| How do spot, dividends and volatility enter an option price? | `BlackScholesMertonProcess`, a European option and the analytic engine; formula, parity and delta checks. | [Options](topics/01-bsm-options/README.md) · [Notebook](topics/01-bsm-options/study.ipynb) |
| How do par quotes become discount factors? | OIS rate helpers and a piecewise curve; quote repricing, zero rates and forwards. | [Yield curves](topics/02-yield-curves/README.md) · [Notebook](topics/02-yield-curves/study.ipynb) |
| What does an inverted curve actually measure? | Par and zero-rate term spreads, then explicit parallel and shape scenarios. | [Curve inversion](topics/03-curve-inversion/README.md) · [Notebook](topics/03-curve-inversion/study.ipynb) |
| How does a bond ticket become a clean price? | A scheduled fixed-rate bond, accrued interest and independent discounted cash flows. | [Bond valuation](topics/04-bond-valuation/README.md) · [Notebook](topics/04-bond-valuation/study.ipynb) |
| Which part of bond risk can a swap offset? | Signed DV01, quote buckets, convexity and frozen-position scenario P&L. | [Bond risk](topics/05-bond-risk/README.md) · [Notebook](topics/05-bond-risk/study.ipynb) |
| Why separate projection from discounting? | Term-swap helpers linked to an OIS discount curve and a single-curve counterfactual. | [Swap curves](topics/06-swap-curves/README.md) · [Notebook](topics/06-swap-curves/study.ipynb) |
| How is an FRA settled and valued? | `IborIndex` and `ForwardRateAgreement`; separate curves, start settlement and buyer/seller signs. | [FRAs](topics/07-forward-rate-agreements/README.md) · [Notebook](topics/07-forward-rate-agreements/study.ipynb) |
| What makes a fixed-for-floating swap fair? | `VanillaSwap`, indexed floating coupons and a discounted fixed-leg annuity. | [Interest rate swaps](topics/08-interest-rate-swaps/README.md) · [Notebook](topics/08-interest-rate-swaps/study.ipynb) |
| How do discount curves imply an FX forward? | Dated USD/EUR cash flows, forward points and covered-interest-parity checks. | [FX forwards](topics/09-fx-forwards/README.md) · [Notebook](topics/09-fx-forwards/study.ipynb) |
| How do two currencies' legs fit together? | Fixed-for-fixed coupon and principal exchanges with explicit reporting currency and zero basis. | [Cross-currency swaps](topics/10-cross-currency-swaps/README.md) · [Notebook](topics/10-cross-currency-swaps/study.ipynb) |
| How do credit spreads imply survival and CDS value? | `SpreadCdsHelper`, a hazard curve and a quarterly `CreditDefaultSwap`; independent premium/default legs. | [Credit default swaps](topics/11-credit-default-swaps/README.md) · [Notebook](topics/11-credit-default-swaps/study.ipynb) |
| What happens when a market quote changes? | `SimpleQuote`, a relinkable curve handle and the same live bond; scenario updates and restoration. | [Quotes, handles and risk](topics/12-quotes-handles-risk/README.md) · [Notebook](topics/12-quotes-handles-risk/study.ipynb) |
| How can a borrower cap floating interest? | `IborLeg`, `Cap`, `Floor` and Black pricing; optionlet reconstruction and cap–floor parity. | [Caps and floors](topics/13-caps-and-floors/README.md) · [Notebook](topics/13-caps-and-floors/study.ipynb) |
| What is the option to enter a swap worth? | A forward swap, European payer/receiver swaptions and `BlackSwaptionEngine`; annuity pricing and parity. | [European swaptions](topics/14-european-swaptions/README.md) · [Notebook](topics/14-european-swaptions/study.ipynb) |

## Choose a learning path

- **Rates and cash bonds:** quotes and handles → yield curves → bond valuation → bond risk → interest rate swaps.
- **Floating-rate and volatility products:** swap curves → FRAs → caps and floors → European swaptions.
- **Currencies and credit:** FX forwards → cross-currency cash flows; then CDS spread calibration and protection legs.

Each notebook shows the instrument construction and the relevant checks. Prices are reconciled to independent formulas or cash-flow sums where feasible; calibration residuals, units and contract limits are reported alongside the result. The short chapters can be explored individually, while the [integrated curve-to-hedge notebook](study.ipynb) connects curve construction, a bond, a swap and scenario risk in one worked case. Its [methods](docs/01-methods.md) and [results](docs/02-results.md) provide the detailed record.

## Research scope

This collection demonstrates practical QuantLib workflows under transparent assumptions. It does not claim live market calibration or executable trading opportunities. The term index is synthetic; FX examples assume compatible collateral and zero currency basis; cross-currency coverage is fixed-for-fixed cash-flow replication. CDS uses a midpoint default engine with explicitly defined quarterly contracts, while caps and swaptions use flat Black volatility assumptions. The chapter notes explain where a desk implementation would need actual contract specifications, fixings, market quotes or richer models.

The original materials are preserved on the `old` branch. The linked chapters form the maintained collection.

[Sources and provenance](research/SOURCES.md) · [Research protocol](research/PROTOCOL.md) · [Further research](research/RESEARCH_AGENDA.md) · [Reproduction details](docs/reproduction.md)
