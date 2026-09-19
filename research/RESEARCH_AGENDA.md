# Further desk research — not yet run

The maintained chapters implement numerical pricing workflows with constructed inputs. Next
steps are market-specific research questions:

- Replace illustrative OIS/term quotes with a dated permitted strip, fixings and contract/CSA
  conventions; study bid/ask, interpolation and time-passing hedge P&L.
- Strip optionlet volatilities from a cap surface and compare shifted-lognormal with normal
  pricing under explicit quote units; calibrate a swaption surface before studying smile risk.
- Compare the implemented midpoint CDS workflow with ISDA test grids and standard contract
  dates, upfront/running-spread conventions and observed credit quotes.
- Extend fixed-for-fixed currency cash flows to floating, basis and resetting-notional
  contracts under an explicit collateral framework.

These are future extensions. The current CDS, cap/floor and swaption notebooks already run
with their declared illustrative contracts; market calibration and production completeness
are separate claims.
