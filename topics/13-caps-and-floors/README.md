# Caps, floors and optionlet risk

Build a floating leg, price its cap and floor with Black, and reconstruct the optionlet values.

[Open the executed notebook](study.ipynb) · [Browse all topics](../../README.md)

A floating-rate borrower can buy a cap to limit interest above a strike; a floor pays when the fixing falls below its strike. QuantLib represents both contracts on a dated `IborLeg`, with projection inherited from its index and discounting supplied by the pricing engine.

The notebook starts a three-year quarterly leg six months after the reference date, notional 100, Actual/360, Modified Following and zero fixing lag. It uses the illustrative dual curves, strike 4%, a flat Black optionlet volatility of 20%, and `BlackCapFloorEngine`. All reset dates are future dates. Indexed coupons are explicit so adjusted accrual periods are not silently substituted for index periods.

For each coupon, the code reads its fixing, value, maturity and payment dates, independently derives its index forward from projection discount factors, and reconstructs the Black caplet/floorlet value using the actual coupon accrual and OIS payment discount. The sum must match each QuantLib instrument. Cap minus floor must equal the discounted floating-minus-fixed coupons. A quote-based volatility sweep then shows the premium response while the contract and curves remain fixed.

Flat optionlet volatility is a constructed assumption, not a cap-volatility surface stripped from quotes. Unshifted Black requires positive forwards and strikes; normal or shifted-lognormal models need separately specified units and conventions. No smile calibration or hedge P&L is claimed. References: [caps and floors API](https://quantlib-python-docs.readthedocs.io/en/latest/instruments/caps.html) and [Black cap/floor engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/capfloor/blackcapfloorengine.cpp).

## What to take away

Independent optionlet sums reproduce both prices, and cap–floor parity reconciles to the linear floating-minus-fixed leg. Raising the assumed volatility increases both premiums while leaving their difference unchanged.

[Source register](../../research/SOURCES.md) · [Full valuation and hedge study](../../study.ipynb)
