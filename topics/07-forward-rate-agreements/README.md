# Forward rate agreements

Connect a forward borrowing rate to the sign and settlement of an FRA.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

An FRA isolates interest on one future borrowing period. The buyer in this chapter receives floating and pays fixed, so a realized fixing above the agreed strike creates a positive settlement amount.

For dates $T_1,T_2$ and accrual $\tau$, the simple projection-implied forward is $L=[P^{proj}(T_1)/P^{proj}(T_2)-1]/\tau$. An end-paid linear interest difference is $N\tau(L-K)$. The standard start-paid FRA transforms that amount into $N\tau(L-K)/(1+\tau L)$ using the observed fixing at $T_1$.

The exercise uses a period from six to nine months after the reference date, notional 100 and Actual/360 accrual. It computes the forward from the illustrative projection curve and compares strikes 50 bp below, at and above it. Under the explicitly deterministic rate-path assumption, it discounts the start settlement with the OIS discount factor to show its current value. The at-forward contract is zero and buyer/seller signs are opposite.

The division by $1+\tau L$ makes start settlement nonlinear in the future fixing. Treating $L$ as a known path value here is an analytical illustration; in a stochastic multi-curve model, replacing that fixing by one simple forward does not by itself price the expectation or settlement convexity. Futures/FRA convexity adjustments, historical fixings, broken dates and actual contract settlement conventions are not estimated.

The chapter therefore teaches rate/strike direction and settlement mechanics without claiming a production FRA engine. Its period and currency conventions are declared rather than inherited from an unrelated index.

## What to take away

At the projected forward, the deterministic FRA has zero settlement value. A higher fixing benefits the receive-floating party. Start settlement differs from an end-paid interest difference and needs an explicit convention.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
