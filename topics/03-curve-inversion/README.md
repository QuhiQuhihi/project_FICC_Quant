# Yield-curve inversion

Separate a negative term spread from a recession forecast.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

An inversion is a statement about the ordering of yields across maturities. A 10Y minus 2Y spread below zero says the selected long rate is below the selected short rate; it does not identify why that shape arose or forecast the date of a recession on its own.

This chapter calculates the spread from the constructed curve in two ways: directly from 10Y and 2Y OIS par quotes, and from the bootstrapped continuously compounded zero rates. It then applies a parallel shift and opposite steepener/flattener shocks to the zero-rate nodes. Reporting the object being shocked avoids mixing a par-quote spread with a zero-rate spread.

The spread is $10^4[z(10)-z(2)]$ basis points. A parallel shift cancels exactly. A shape shock changes the spread according to the difference between the long- and short-node shocks. This simple identity is checked in the notebook, while the figure compares the entire constructed zero curve rather than only two points.

Scenario nodes are deterministic illustrations, not historical observations or newly calibrated par instruments. The exercise does not estimate recession probabilities, term premia, policy expectations or the profitability of a curve trade. A historical prediction study would need a dated public yield series, a defined target and forecast horizon, release-vintage treatment and a genuinely later evaluation period. Those are distinct research questions from measuring an inversion.

## What to take away

The parallel shock changes the level but leaves the term spread unchanged. Steepening and flattening change the spread by construction; none of these scenarios supplies recession evidence.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
