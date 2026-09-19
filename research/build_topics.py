"""Build topic notebooks with fresh kernels and atomic per-chapter saves."""

import argparse
import json
import os
from pathlib import Path
import sys

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.common import provenance, sha  # noqa: E402
from research.topic_content import TOPICS  # noqa: E402

SETUP = """from pathlib import Path
import sys
candidates = [Path.cwd(), *Path.cwd().parents]
ROOT = next(p for p in candidates if (p / 'research' / 'pricing.py').is_file())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import QuantLib as ql
from IPython.display import display
from research.common import RESULTS, check_hashes
from research.pricing import DATE, CAL, valuation_date, curves, fixture
plt.rcParams.update({'figure.dpi':110, 'axes.spines.top':False, 'axes.spines.right':False,
                     'axes.grid':True, 'grid.alpha':.18, 'font.size':11})
# Verify the core fixture, source and saved-output vintage before reading any summary.
check_hashes()
# Every chapter uses explicit illustrative assumptions; never a hidden data download.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=[c["slug"] for c in TOPICS])
    args = parser.parse_args()
    for key, directory in [
        ("MPLCONFIGDIR", "matplotlib"),
        ("IPYTHONDIR", "ipython"),
        ("JUPYTER_CONFIG_DIR", "jupyter"),
        ("JUPYTER_DATA_DIR", "jupyter_data"),
        ("JUPYTER_RUNTIME_DIR", "jupyter_runtime"),
    ]:
        path = ROOT / ".cache" / directory
        path.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault(key, str(path))
    destination = ROOT / "research/topics_manifest.json"
    records = json.loads(destination.read_text()).get("topics", {}) if destination.exists() else {}
    for chapter in TOPICS:
        if args.topic and args.topic != chapter["slug"]:
            continue
        folder = ROOT / "topics" / chapter["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        md, code = nbformat.v4.new_markdown_cell, nbformat.v4.new_code_cell
        readme = (
            "# "
            + chapter["title"]
            + "\n\n"
            + chapter["teaser"]
            + "\n\n[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)\n\n"
            + chapter["body"]
            + "\n\n## What to take away\n\n"
            + chapter["conclusion"]
            + "\n\n[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)\n"
        )
        nb = nbformat.v4.new_notebook()
        nb.metadata.kernelspec = {
            "name": "python3",
            "display_name": "Python 3",
            "language": "python",
        }
        nb.cells = [
            md(
                "# "
                + chapter["title"]
                + "\n\n"
                + chapter["teaser"]
                + "\n\n[Chapter notes](README.md) · [All topics](../../README.md)"
            ),
            md("## Research design\n\n" + chapter["body"]),
            code(SETUP),
            md(
                "## Calculation and independent checks\n\nAll inputs below are illustrative. Assertions check the identities discussed in the chapter."
            ),
            code(chapter["calculation"].strip()),
            md("## Economic relationship"),
            code(chapter["figure"].strip()),
            md("## Interpretation\n\n" + chapter["conclusion"]),
        ]
        NotebookClient(
            nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(folder)}}
        ).execute()
        nbformat.validate(nb)
        temporary = folder / "study.ipynb.partial"
        nbformat.write(nb, temporary)
        temporary.replace(folder / "study.ipynb")
        (folder / "README.md").write_text(readme)
        html, _ = HTMLExporter().from_notebook_node(nb)
        preview = ROOT / "research/preview/topics"
        preview.mkdir(parents=True, exist_ok=True)
        (preview / (chapter["slug"] + ".html")).write_text(html)
        records[chapter["slug"]] = {
            "title": chapter["title"],
            "kind": chapter["kind"],
            "notebook": str((folder / "study.ipynb").relative_to(ROOT)),
            "notebook_sha256": sha(folder / "study.ipynb"),
            "readme_sha256": sha(folder / "README.md"),
            "source_and_code": provenance(),
            "executed_code_cells": 3,
        }
        destination.write_text(json.dumps({"topics": records}, indent=2) + "\n")
        print("Executed " + chapter["slug"], flush=True)
    print("Saved complete notebooks and local HTML previews; refresh the connected study next.")


if __name__ == "__main__":
    main()
