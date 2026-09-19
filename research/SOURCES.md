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

## Topic collection references and assumptions

- [QuantLib analytic European engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/vanilla/analyticeuropeanengine.cpp), reviewed 19 September 2026: primary implementation reference for the option formula comparison.
- [BIS, Covered interest parity lost](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis), reviewed 19 September 2026: currency funding/basis context; no empirical figures or data are reproduced.
- [ISDA CDS Standard Model](https://www.cdsmodel.com/), reviewed 19 September 2026: identifies the standard-contract comparison needed beyond this chapter's continuous-premium illustration. No ISDA implementation or test-grid match is claimed.

Additional authored assumptions are visible in [topic sources](topic_content.py) and each
notebook: BSM spot/strike 100, one year, continuous r=4%, q=1%, volatility=20%; a separate
October accrued-interest example with flat 3.5%; six-to-nine-month deterministic FRA;
five-year fixed-for-fixed currency legs with USD 4%, EUR 2.5% and zero basis; five-year
continuous-premium CDS with r=3.5%, hazard=2%, recovery=40%. They are constructed teaching
inputs, not downloaded series, observations or empirical evidence.
