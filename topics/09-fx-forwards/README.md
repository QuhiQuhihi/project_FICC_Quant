# FX forwards and covered interest parity

Price a future currency exchange with dated domestic and foreign cash flows.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

An FX forward fixes the exchange rate for a future currency exchange. To keep signs visible, spot and strike are quoted as USD per EUR, and the position receives one EUR and pays $K$ USD at maturity.

Under zero basis and compatible collateral assumptions,

$$F=S\frac{D_{EUR}}{D_{USD}},\qquad PV_{USD}=S D_{EUR}-K D_{USD}.$$

The exercise uses spot 1.10 USD/EUR, the constructed USD curve and an illustrative flat continuously compounded EUR rate of 2.5%. At the fair forward, discounted payments cancel. Strikes 0.01 below and above fair value expose the sign of a long-EUR forward. A one-to-ten-year table connects the interest-rate difference to forward points.

Forward points are quoted in $10^{-4}$ USD/EUR in this notebook, so a point equals 0.0001 in the outright exchange rate. The strike is not an expected future spot forecast: it is the rate implied by the chosen no-basis discount factors and replication assumptions.

The numerical parity identity does not establish an executable arbitrage. Observed forward prices can also reflect collateral, funding, balance-sheet costs, bid/ask and currency basis. Those inputs are not supplied here. The [BIS discussion of covered interest parity](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis) motivates treating zero basis as an assumption rather than an observed market fact.

## What to take away

All fair forwards have zero discounted PV under the stated no-basis assumptions. A lower agreed USD strike benefits a long-EUR forward; forward points are not a forecast of the future spot rate.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
