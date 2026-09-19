# Reproducing the research

[Return to the research overview](../README.md).

Use Python 3.12 and the committed `uv.lock` in a Linux environment. All FICC inputs are versioned illustrative assumptions; no vendor download or credentials are required.

```bash
uv sync --locked
uv run python research/run_study.py
uv run python research/build_topics.py
uv run python research/build_notebook.py
uv run python research/check_artifacts.py
```

The first command after setup rebuilds the connected curve/valuation/hedge study. The topic builder executes all eleven chapters in fresh kernels and saves each notebook only after its calculations and assertions succeed. The final builder refreshes the connected study and its provenance after the topic artifacts are available.

After a source or assumption change, rebuild `research/run_study.py` first so the source and fixture checks match the new study. To rerun one chapter, use `uv run python research/build_topics.py --topic 07-forward-rate-agreements`. Finish with `research/build_notebook.py` and `research/check_artifacts.py` so the aggregate evidence remains current. Rebuilding a chapter refreshes its README from the authored narrative in `research/topic_content.py`; edit that source when revising a chapter.

Outputs are the root `study.ipynb`, `topics/*/study.ipynb`, summary evidence under `research/results/`, and local HTML previews under `research/preview/`. Every notebook discovers the repository from its own directory or the repository root. A failed execution leaves the last completed notebook intact; rerun the same command to recover.

Numerical and repository checks:

```bash
uv run python -m pytest -q
uv run python -m ruff check research tests
uv run python -m ruff format --check research tests
uv run python research/check_artifacts.py --public
```

The public check validates chapter coverage, local links, executed notebooks and recorded topic hashes. Full artifact checking additionally reconciles saved cash flows, risk measures and the core source/fixture hashes. Passing checks validates these numerical experiments; it does not establish empirical market accuracy or product completeness.
