# Acceptance evidence — 19 September 2026

| Brief criterion | Evidence and boundary |
|---|---|
| Original components and clear question | [Audit](AUDIT.md), per-file [legacy inventory](legacy_inventory.json), original `old` branch; retained/replaced/archived claims distinguished. |
| Versioned appropriate inputs | [Sources](SOURCES.md), [manifest](data/input_manifest.json), pinned hashes. Raw market snapshots require permitted local access; FICC uses a committed constructed fixture. |
| Study actually executed | [Executed notebook](../study.ipynb), [machine-readable summaries](results/), [generated results](../docs/02-results.md). |
| Meaningful comparisons | [Protocol](PROTOCOL.md) and [methods](../docs/01-methods.md) define timing, universe/risk controls or pricing conventions. |
| Consequential defects handled | [Audit](AUDIT.md) connects defects to maintained replacements or withdrawn legacy claims. |
| Numerical/timing/accounting checks | Independent cash-flow PV, clean/dirty identity, calibration/parity, signed risks and negative-rate cases; 5 tests. `research/check_artifacts.py` additionally reconciles saved artifacts independently. |
| Uncertainty and sensitivity | Quote repricing and PV tolerances, 0.1/1/5 bp risk convergence, curve/convention comparisons and five frozen scenarios. |
| Headline consistency | Generated integrated-case results, its notebook and saved headline agree. The overview introduces fourteen desk chapters and links to the numerical case rather than embedding a selected hedge result. |
| Environment and executable report | Locked offline sync, lint/format and 5 tests pass; 15 executed notebooks: 56 code cells, 18 embedded figures and no cell errors, including 14 topic chapters. |
| Reproduction and CI | [Reproduction details](../docs/reproduction.md), ignored cached inputs and recoverable checkpoints; CI checks synthetic/public artifacts, not restricted historical reproduction. |
| Maintained files and attribution | `.gitignore` excludes raw/recovery/environment paths; [NOTICE](../NOTICE) retains attribution. Original history is preserved rather than rewritten. |
| Publication boundary | [PUBLICATION.md](../PUBLICATION.md): local artifacts checked; no live publication or complete historical rights/credential clearance. |
| Supported conclusion and next experiment | The one-swap hedge removes parallel first-order risk but retains shape/convexity exposure; inputs are illustrative. [Agenda](RESEARCH_AGENDA.md) is explicitly unrun. |

All completed checks refer to local execution. Provider data accuracy, point-in-time vintages,
actual transaction execution and unrestricted redistribution are not certified. See the
[work log](WORKLOG.md) for commands, recovery and the visual/HTML inspection boundary.

## Topic collection acceptance

Every original topic has a direct [overview link](../README.md), detailed chapter README and
freshly executed notebook; three new chapters extend the collection to fourteen topics.
Checks cover BSM engine/formula/parity agreement, curve calibration, term-spread scenarios,
accrued-interest identity, rate derivatives, projection alternatives, QuantLib FRA settlement
and opposite positions, swap annuity, FX parity and currency principal/coupon balance.

The desk extension independently reconciles scheduled CDS premiums, default accrual and
protection values, checks the credit helper strip and survival, and reprices the ticket at
its own fair spread. Quote updates and curve relinks restore their starting state and match
analytic discounting/DV01. Cap/floor optionlets match direct Black formulas and parity;
European payer/receiver swaption prices match the Black annuity formula and forward-swap PV.
The notebook checker requires every chapter, validates links and verifies source/output hashes.

FRA forward substitution, fixed-for-fixed currency cash flows, midpoint credit integration
and flat Black volatility assumptions retain their stated limits. These examples demonstrate
QuantLib implementation and numerical consistency, not market or production completeness.
