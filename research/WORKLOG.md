# Renovation work log

Started 2026-09-19 in WSL as daham. Original commit `37b2bf84e6f5af5508bed2cb4d5d4b5346259f44` is preserved on `old`; active branch `renovation`. No remote operations.

Reference inspected: corporate-bond project at `1f565f6d7010274ff8feb333b9c05be11ba1dcfa`, README, protocol, sources, evaluation, agenda, publication review.

Initial phase: audit and protocol, before primary evaluation. Outputs: `research/results/`, `research/figures/`, `study.ipynb`; raw snapshots stay ignored in `research/data/raw/`. Reruns overwrite only generated artifacts. Notebook replaced atomically after successful clean-kernel execution.

Recovery: `uv sync --locked`; `uv run python research/acquire.py` (data projects); `uv run python research/run_study.py`; `uv run python research/build_notebook.py`; `uv run pytest -q`; `uv run python research/check_artifacts.py`. Acquisition reuses valid per-ticker hashes and stops on changed sources.

## Completed verification — 19 September 2026 KST

- `uv sync --locked --offline`: succeeded using the installed Linux Python 3.12 environment and cached dependencies.
- Constructed fixture verified against its committed SHA-256; no observed swap market data claimed.
- `uv run python research/run_study.py`: completed numerical study; the notebook build also reran its maintained entry point.
- `uv run python research/build_notebook.py`: successful fresh-kernel execution, 14 code cells, 4 embedded quantitative figures, zero cell errors. Notebook headline matches generated results. HTML preview has embedded figures and tables.
- `uv run python -m pytest -q`: **5 passed**.
- `uv run python -m ruff check research tests` and `uv run python -m ruff format --check research tests`: passed.
- `uv run python research/check_artifacts.py`: public links/notebook checks, current source/code/output hashes and independent saved-output calculations passed.
- All 4 generated PNGs inspected; exact sample/convention labels checked. HTML structure inspected programmatically; no full browser/site layout certification.

The exact final numerical conclusions are in [generated results](../docs/02-results.md).
[Acceptance evidence](ACCEPTANCE.md) records coverage and boundaries. Local checks exercise the
committed CI commands; no remote GitHub workflow, push, deployment or live blog publication was run.
The maintained Git tree omits raw vendor histories, ignored recovery material, environments and
caches. Historical credential/rights boundaries remain in [publication review](../PUBLICATION.md).

Final Git review: original `old` reference verified; maintained Markdown links resolve within the staged tree. Tracked evidence hashes match staged bytes, and raw/recovery/environment paths are absent. `.gitattributes` preserves Linux source line endings and exact hashed CSV serializer bytes. Staged whitespace checks pass.

## Research presentation and topic collection — 19 September 2026

The README now introduces the economic research questions and all eleven original subject
areas, with direct links to each chapter's notes and notebook. Setup commands moved to
`docs/reproduction.md`. The main pipeline updates only the explicitly marked numerical
result paragraph and preserves the authored introduction and navigation.

Output/recovery: `topics/*/README.md` and `topics/*/study.ipynb`; source narratives and visible
calculations in `research/topic_content.py`; per-chapter execution provenance in
`research/topics_manifest.json`; ignored HTML previews under `research/preview/topics/`.
The builder saves one fully executed chapter at a time, so failed runs preserve earlier
completed artifacts. Recovery is `research/run_study.py`, `research/build_topics.py`
(optionally `--topic <slug>`), then `research/build_notebook.py` and `research/check_artifacts.py`.
Each chapter checks the pinned core fixture/source/output vintage before calculations.

The complete first execution passed all analytical assertions in eleven fresh kernels.
All eleven chapter figures were inspected; two legends were changed from internal column
names to research labels, followed by final regeneration. The primary bond, hedge and
scenario results are unchanged. New options, FRA, currency and credit calculations are
explicitly illustrative teaching exercises with boundaries stated in each chapter.

Final topic-collection checks passed: `research/build_topics.py` executed all 11 chapters;
`research/build_notebook.py` executed the connected study again; `research/check_artifacts.py`
and its `--public` mode validated 12 notebooks, 47 executed code cells, chapter/source hashes,
local Markdown/notebook links and independent core calculations. There are 15 embedded
figures in total. All 11 chapter figures were inspected, including the corrected legends;
11 HTML previews were checked for embedded image/table structure. No full browser-layout
certification is claimed. The 5 existing pricing tests and Ruff lint/format checks pass.
The README introduction and all 11 notebook navigation links remain intact after regeneration;
its result block matches the generated result paragraph. No subtask commit or push was made.

Independent-review correction: the inversion notebook now asserts the steepener and flattener spread-change identities and the independently expected +88.8889/-88.8889 bp changes. All chapter notebooks and the connected study were regenerated for the changed shared source fingerprint. Full/public artifact checks pass again: 12 notebooks, 47 executed code cells, valid hashes/links and reconciled calculations. Primary valuation and hedge results are unchanged.

## QuantLib desk direction — 19 September 2026

The user requested practical QuantLib coverage rather than a featured one-swap hedge result.
The root README now introduces fourteen desk questions with brief descriptions, specific
QuantLib objects and direct links to notes and notebooks. It includes three learning paths.
The integrated bond/swap case remains linked evidence; `run_study.py` no longer injects its
numerical result into the overview.

Five substantive workflows were added or expanded. FRA now instantiates the library's
contract using the locked index-first constructor and checks independent start settlement,
discounted PV and opposite positions. CDS now bootstraps illustrative spread helpers and
prices an explicit quarterly contract; separate midpoint cash-flow sums reconcile scheduled
premiums, default accrual, protection and total PV. New chapters expose quote notifications
and curve relinking, cap/floor optionlet pricing and European swaption annuity pricing.
All inputs are illustrative and each chapter distinguishes its contract/model conventions
from a complete market implementation. Primary QuantLib API/source references were checked.

Canonical desk content is `research/desk_content.py`, imported by `research/topic_content.py`.
Output/recovery remains one atomic `topics/<slug>/study.ipynb` and README per successful
chapter, plus `research/topics_manifest.json` and ignored HTML previews. The complete replay
is `research/run_study.py`, `research/build_topics.py`, then `research/build_notebook.py`.
Source fingerprints include the new content module and protocol amendment; metadata was
regenerated from calculations rather than hand-edited.

Final execution evidence: all 14 topic notebooks and the integrated notebook executed in
fresh kernels without cell errors: 15 notebooks, 56 code cells, 18 embedded figures.
`research/check_artifacts.py` passed both public-file/topic checks and independent saved-output
reconciliation with current source hashes. All 5 existing pricing tests passed; Ruff lint,
Ruff format and `git diff --check` passed. All five new/expanded figures were inspected;
all 14 topic HTML previews contain embedded images and result tables. No browser-layout
certification is claimed. The README retains fourteen direct notebook links after regeneration.
The integrated valuation/hedge results are unchanged. Agent/Codex instruction names remain
ignored. No subtask commit or push was made; publication is handled by the parent task.
