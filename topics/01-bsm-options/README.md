# Black–Scholes–Merton options

How volatility, moneyness and dividends shape European option values.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A European call separates upside participation from ownership of the underlying. The question here is how much that convex payoff is worth when volatility, financing and dividends are specified, and which input drives a local hedge.

For spot $S$, strike $K$, maturity $T$, continuous rates $r,q$ and volatility $\sigma$,

$$C=Se^{-qT}\Phi(d_1)-Ke^{-rT}\Phi(d_2),\qquad d_1=\frac{\log(S/K)+(r-q+\sigma^2/2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T.$$

The exercise fixes $S=K=100$, $T=1$, $r=4\%$, $q=1\%$ and $\sigma=20\%$. A direct normal-distribution formula is compared with QuantLib's analytic European engine; call–put parity and a finite-difference delta provide separate checks. A volatility sweep shows the economic role of convexity.

Delta is measured per unit of spot. Vega describes a change in volatility, so a one-percentage-point volatility move is 0.01 in the formula's decimal units. These are model sensitivities under a constant-volatility diffusion; they do not estimate implied volatility, realized hedge costs, jump risk or a volatility smile. The contract is European and pays a continuous dividend yield; discrete dividends and American exercise need other models.

[QuantLib's analytic engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/vanilla/analyticeuropeanengine.cpp) is the implementation reference; all numerical inputs are original illustrative assumptions.

## What to take away

The formula, QuantLib price and parity agree. The increasing value across the volatility sweep reflects the convex call payoff under this model; it is not an empirical volatility premium.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
