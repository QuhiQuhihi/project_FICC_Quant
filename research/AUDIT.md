# Audit — 19 September 2026

Starting commit: `37b2bf84e6f5af5508bed2cb4d5d4b5346259f44` (branch `old`). Clean status verified before edits. All root notebooks inspected as JSON without execution; README, helper modules, data inventory and source schemas inspected. Saved outputs are not validation.

Original: eleven educational notebooks covering BSM options, Treasury curves/inversion/pricing/risk, swap curves, FRA, IRS, FX forwards, cross-currency swaps and CDS, plus four helper modules and undocumented spreadsheets/screenshots.

Verified defects:
- `quant_lib/cds_curve.py:13,23` hard-code another checkout; helpers rely on mutable global evaluation dates.
- `quant_lib/cds_curve.py:76–85` replaces a list with FuturesRateHelper and then calls append on that helper; construction fails when futures are present. Equivalent pattern occurs in the swap notebook.
- `quant_lib/cds_curve.py:95` uses Euribor3M while naming inputs USD IRS; currencies/calendars cannot be reconciled by relabeling the output.
- `7_forward_rate_agreement.ipynb`, cell 2 assigns the short-side attribute `postion`, not `position`.
- Notebook/helper uses of `UnitedStates()` and `ActualActual()` omit explicit conventions required by the current supported bindings; tests will validate the new explicit APIs.
- `2_yield_curve.ipynb` and its inversion copy scrape mutable WSJ pages without frozen quotes or hashes. Saved output does not establish reproducibility.

Disposition: yield/swap curves, bond pricing/risk and IRS become the connected core; FX forward parity becomes validated supporting material. BSM, FRA, cross-currency and CDS remain archived educational context, not validated current coverage. Cross-currency basis, collateral, recovery, fixings and product-specific settlement evidence are missing; no claim of complete product coverage. Vendor spreadsheets and screenshots have no established redistribution permissions and are excluded from the maintained tree. `legacy_inventory.json` maps every original file.

Scope: dated, explicitly constructed SOFR-style OIS quotes and a synthetic USD 3-month term index permit numerical model validation. These are not observed market prices or current traded USD LIBOR. A bond, dual-curve term swap and frozen hedge demonstrate convention/model risk. The NY Fed overnight reference is not a complete swap quote set; Treasury par yields are not used as a collateral discount curve. Empirical mispricing or executable arbitrage is outside the completed numerical study.

Recovery: `git show old:<path>` or ignored `research/private-legacy/<path>`. Original history is intentionally preserved, not publication-cleared.

Presentation supplement: the maintained research collection now restores navigation across
all eleven original subject areas with newly authored notes and executed illustrative
notebooks. This supersedes the earlier archival-only disposition for introductory BSM, FRA,
cross-currency and CDS coverage; it does not validate the legacy implementations or data.


QuantLib desk supplement: fourteen maintained chapters now lead the project. FRA constructs
a real `ForwardRateAgreement`; CDS bootstraps a hazard curve and prices a discrete quarterly
contract with independent midpoint leg reconciliation. New chapters cover observable quotes
and relinkable handles, caps/floors with optionlet sums, and European physical swaptions.
This supersedes the analytical-only FRA/CDS scope in the earlier supplement, while retaining
explicit model/contract limits. It does not rehabilitate legacy code or vendor inputs.
The root overview introduces practical desk questions and links every chapter; numerical
hedge outcomes remain in the integrated case rather than being injected into the overview.
