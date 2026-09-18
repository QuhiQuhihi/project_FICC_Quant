# Sources and input provenance

Reviewed 19 September 2026. External source statements, modeling assumptions and computed
results are kept separate. No paper's reported performance is presented as reproduced here.
The corporate-bond quality reference was inspected locally at commit
`1f565f6d7010274ff8feb333b9c05be11ba1dcfa` (README, protocol, sources, evaluation, agenda, publication).

## Constructed numerical inputs

[illustrative_quotes.csv](data/illustrative_quotes.csv) contains original hypothetical decimal
par rates for 1–10-year tenors, with a checksum in [input_manifest.json](data/input_manifest.json).
Created 19 September 2026; valuation date assumed 15 September. These are not retrieved quotes,
executable prices, historical fixings or a fitted empirical market surface.

Legacy spreadsheets and screenshots lack adequate vendor, retrieval, collateral and quote
convention records. Their redistribution rights are unestablished. They remain in local
recovery/original history and are not numerical inputs. No synthetic input substitutes for a
claimed empirical study: the completed scope is numerical valuation/hedge validation.

## Primary technical sources

- [QuantLib official documentation](https://www.quantlib.org/docs.shtml), with the [official Python binding tests](https://github.com/lballabio/QuantLib-SWIG/blob/master/Python/test/test_ratehelpers.py): helper and valuation APIs. Installed QuantLib 1.43 signatures were inspected and calls executed; separate discounting and indexed-coupon choices are explicit.
- [New York Fed SOFR documentation](https://www.newyorkfed.org/markets/reference-rates/sofr): defines the overnight secured rate and its publication conventions. It does not provide the illustrative term/OIS quote strip used here. No observed SOFR level is inserted as a market term curve.

Contribution: a connected input/convention/calibration/cash-flow/risk/hedge experiment,
independent PV and zero-spread checks, and a quantified indexed-coupon convention correction.
Internal repricing accuracy, numerical error, model risk and execution economics remain separate.
