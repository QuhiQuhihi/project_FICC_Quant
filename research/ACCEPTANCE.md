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
| Headline consistency | The explicit result block in the research-first README, generated results, connected notebook and saved headline agree; the editorial introduction is preserved by regeneration. |
| Environment and executable report | Locked offline sync, lint/format and 5 tests pass; 12 executed notebooks: 47 code cells, 15 embedded figures and no cell errors, including 11 topic chapters. |
| Reproduction and CI | [Reproduction details](../docs/reproduction.md), ignored cached inputs and recoverable checkpoints; CI checks synthetic/public artifacts, not restricted historical reproduction. |
| Maintained files and attribution | `.gitignore` excludes raw/recovery/environment paths; [NOTICE](../NOTICE) retains attribution. Original history is preserved rather than rewritten. |
| Publication boundary | [PUBLICATION.md](../PUBLICATION.md): local artifacts checked; no live publication or complete historical rights/credential clearance. |
| Supported conclusion and next experiment | The one-swap hedge removes parallel first-order risk but retains shape/convexity exposure; inputs are illustrative. [Agenda](RESEARCH_AGENDA.md) is explicitly unrun. |

All completed checks refer to local execution. Provider data accuracy, point-in-time vintages,
actual transaction execution and unrestricted redistribution are not certified. See the
[work log](WORKLOG.md) for commands, recovery and the visual/HTML inspection boundary.

## Topic collection acceptance

Every original topic has a direct [overview link](../README.md), detailed chapter README and
freshly executed notebook. Analytical checks cover BSM engine/formula/parity agreement,
curve calibration, term-spread invariance, accrued-interest identity, independent rate
derivatives, projection alternatives, FRA settlement, swap annuity, FX parity, currency
principal/coupon balance and continuous-premium CDS valuation. The notebook checker requires
all eleven topics, validates Markdown links and verifies chapter/source hashes. Simplified
FRA, fixed-for-fixed currency and continuous-premium credit cases state their contract/model
boundaries locally; they do not assert complete production or market validation.
