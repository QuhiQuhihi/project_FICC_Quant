"""Visible QuantLib desk workflows with explicit illustrative contracts and checks."""

FRA = {
    "slug": "07-forward-rate-agreements",
    "title": "Forward rate agreements in QuantLib",
    "teaser": "Construct a receive-floating FRA, separate projection from discounting, and reconcile start settlement.",
    "body": r"""A desk FRA locks the rate for one future borrowing period. Here the long position receives floating and pays fixed on notional 100. It starts six months after 15 September 2026 and ends three index months later. The synthetic USD 3M index has zero fixing lag, Modified Following dates and Actual/360 accrual; it is not a live traded benchmark.

The notebook builds `IborIndex`, two `YieldTermStructureHandle` objects and `ForwardRateAgreement`. The index supplies projection; a separate handle supplies OIS discounting. The explicit-maturity constructor uses a discount-ratio forward. Choosing the end date from `index.maturityDate(start)` keeps this example aligned with the index period.

For the projected rate $L$, strike $K$ and accrual $\tau$, start settlement is $N\tau(L-K)/(1+\tau L)$. We reconstruct this amount and its discounted PV independently, check buyer/seller symmetry, and compare strikes 50 bp below, at and above the forward. QuantLib's constructor order is checked against the installed locked version; older Python examples can use a different order.

This is the library's deterministic forward substitution, not a stochastic settlement-convexity model. All fixings are future dates, so no historical fixing is silently supplied. A production ticket also needs its actual index, fixing availability, broken-date treatment and legal settlement convention. See the [QuantLib FRA implementation](https://github.com/lballabio/QuantLib/blob/master/ql/instruments/forwardrateagreement.cpp).""",
    "calculation": r"""
with valuation_date():
    discount, projection, _ = curves()
    discount_handle = ql.YieldTermStructureHandle(discount)
    projection_handle = ql.YieldTermStructureHandle(projection)
    index = ql.IborIndex('IllustrativeDesk3M', ql.Period('3M'), 0,
                        ql.USDCurrency(), CAL, ql.ModifiedFollowing, False,
                        ql.Actual360(), projection_handle)
    start = CAL.advance(DATE, ql.Period('6M'))
    end = index.maturityDate(start)
    tau = index.dayCounter().yearFraction(start, end)
    forward = (projection.discount(start)/projection.discount(end)-1)/tau
    rows = []
    for spread in [-.005, 0., .005]:
        strike = forward + spread
        buyer = ql.ForwardRateAgreement(index, start, end, ql.Position.Long,
                                       strike, 100., discount_handle)
        seller = ql.ForwardRateAgreement(index, start, end, ql.Position.Short,
                                        strike, 100., discount_handle)
        settlement = 100*tau*(forward-strike)/(1+tau*forward)
        manual_pv = settlement*discount.discount(start)
        assert abs(buyer.forwardRate().rate()-forward) < 1e-12
        assert abs(buyer.amount()-settlement) < 1e-12
        assert abs(buyer.NPV()-manual_pv) < 1e-12
        assert abs(buyer.NPV()+seller.NPV()) < 1e-12
        rows.append({'strike_pct':100*strike, 'forward_pct':100*forward,
                     'start_settlement':settlement, 'manual_PV':manual_pv,
                     'QuantLib_PV':buyer.NPV()})
    fra = pd.DataFrame(rows)
assert abs(fra.iloc[1].QuantLib_PV) < 1e-12
assert fra.iloc[0].QuantLib_PV > 0 > fra.iloc[2].QuantLib_PV
print(f'Accrual {start.ISO()} to {end.ISO()}; Actual/360 fraction {tau:.6f}')
display(fra.round(6))
""",
    "figure": r"""
fixings = np.linspace(max(-.01, forward-.02), forward+.02, 80)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(100*fixings, 100*tau*(fixings-forward)/(1+tau*fixings), color='#315b7d')
ax.axhline(0, color='#555555', lw=.8)
ax.axvline(100*forward, color='#bc6c25', ls='--', label='Frozen strike')
ax.set(xlabel='Illustrative realized fixing (%)', ylabel='Start settlement per 100',
       title='FRA settlement: receive floating, pay fixed')
ax.legend(); fig.tight_layout(); plt.show()
""",
    "conclusion": "QuantLib agrees with independently calculated start settlement and discounted PV. The at-forward FRA is zero; reversing the position reverses value. Projection and discounting remain separate inputs.",
    "kind": "Illustrative QuantLib desk workflow",
}

CDS = {
    "slug": "11-credit-default-swaps",
    "title": "CDS hazard calibration and credit legs",
    "teaser": "Bootstrap survival from a spread strip, price a quarterly CDS, and reconcile premium and protection legs.",
    "body": r"""A credit desk needs more than the approximation spread ≈ loss-given-default × hazard. A CDS curve must reproduce quoted contracts under declared premium, default and settlement conventions.

This notebook constructs illustrative 1Y, 3Y and 5Y spreads of 80, 110 and 140 bp with recovery 40%, then uses `SpreadCdsHelper` and `PiecewiseFlatHazardRate`. The discount curve is the collection's OIS fixture. Helpers use zero settlement days, quarterly premiums, Following, Forward schedule generation and Actual/360. Helper implied quotes must match the input strip within $10^{-8}$ decimal rate units. Survival must remain between zero and one and decrease with maturity.

Next, `CreditDefaultSwap` and `MidPointCdsEngine` value a separate five-year protection-buyer ticket with running premium 100 bp, notional 100, protection starting on the reference date, quarterly Forward schedule, Actual/360, premium accrued on default, payment at default, no accrual rebate and zero cash-settlement days. It is intentionally an off-market ticket, not an assertion that its conventions equal every calibration-helper convention. The notebook independently sums survival-weighted premiums, accrued premium at midpoint default and loss-given-default payments; it then reprices the ticket at its own fair spread.

Midpoint default integration is a numerical approximation. This example is not an ISDA Standard Model validation and uses neither standard IMM contracts nor observed credit quotes. Hazard is a pricing-measure input, not a physical default forecast. References: [QuantLib Python CDS example](https://github.com/lballabio/QuantLib-SWIG/blob/master/Python/examples/cds.py), [midpoint engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/credit/midpointcdsengine.cpp), and [ISDA model](https://www.cdsmodel.com/).""",
    "calculation": r"""
with valuation_date():
    discount, _, _ = curves()
    discount_handle = ql.YieldTermStructureHandle(discount)
    recovery, notional, running = .40, 100., .01
    tenors, spreads = [1, 3, 5], [.008, .011, .014]
    helpers = [ql.SpreadCdsHelper(s, ql.Period(y, ql.Years), 0, CAL,
               ql.Quarterly, ql.Following, ql.DateGeneration.Forward,
               ql.Actual360(), recovery, discount_handle)
               for y, s in zip(tenors, spreads)]
    hazard_curve = ql.PiecewiseFlatHazardRate(DATE, helpers, ql.Actual365Fixed())
    probability = ql.DefaultProbabilityTermStructureHandle(hazard_curve)
    # Trigger the lazy bootstrap before asking helpers for implied quotes.
    hazard_curve.survivalProbability(DATE + ql.Period('5Y'))
    calibration = pd.DataFrame({'tenor_years':tenors, 'input_bp':1e4*np.array(spreads),
                               'implied_bp':[1e4*h.impliedQuote() for h in helpers]})
    assert np.max(np.abs(calibration.input_bp-calibration.implied_bp)) < 1e-4
    schedule = ql.Schedule(DATE, DATE+ql.Period('5Y'), ql.Period('3M'), CAL,
                           ql.Following, ql.Following, ql.DateGeneration.Forward, False)
    def contract(spread):
        instrument = ql.CreditDefaultSwap(ql.Protection.Buyer, notional, spread,
            schedule, ql.Following, ql.Actual360(), True, True, DATE,
            ql.FaceValueClaim(), ql.Actual360(), False, DATE, 0)
        instrument.setPricingEngine(ql.MidPointCdsEngine(probability, recovery, discount_handle))
        return instrument
    cds = contract(running)
    rows = []
    for flow in cds.coupons():
        coupon = ql.as_coupon(flow)
        start, end, pay = coupon.accrualStartDate(), coupon.accrualEndDate(), coupon.date()
        midpoint = start + (end-start)//2
        dp = hazard_curve.survivalProbability(start)-hazard_curve.survivalProbability(end)
        scheduled = (notional*running*ql.Actual360().yearFraction(start,end)
                     *hazard_curve.survivalProbability(pay)*discount.discount(pay))
        accrued = (notional*running*ql.Actual360().yearFraction(start,midpoint)
                   *dp*discount.discount(midpoint))
        protection = notional*(1-recovery)*dp*discount.discount(midpoint)
        rows.append({'payment':pay.ISO(), 'scheduled_premium_PV':scheduled,
                     'default_accrual_PV':accrued, 'protection_PV':protection})
    legs = pd.DataFrame(rows)
    premium = legs.scheduled_premium_PV.sum()+legs.default_accrual_PV.sum()
    protection = legs.protection_PV.sum()
    assert abs(-premium-cds.couponLegNPV()) < 1e-10
    assert abs(protection-cds.defaultLegNPV()) < 1e-10
    assert abs(protection-premium-cds.NPV()) < 1e-10
    assert abs(contract(cds.fairSpread()).NPV()) < 1e-10
    survival = pd.DataFrame([{'years':y, 'survival':hazard_curve.survivalProbability(DATE+ql.Period(y,ql.Years))}
                             for y in range(0,6)])
    assert ((survival.survival > 0)&(survival.survival <= 1)).all()
    assert (np.diff(survival.survival) <= 0).all()
    summary = pd.DataFrame([{'running_bp':running*1e4, 'fair_ticket_spread_bp':cds.fairSpread()*1e4,
                'buyer_PV':cds.NPV(), 'manual_PV':protection-premium,
                'premium_PV':premium, 'protection_PV':protection}])
display(calibration.round(6)); display(summary.round(6)); display(legs.round(6))
""",
    "figure": r"""
fig, axes = plt.subplots(1,2,figsize=(10,4))
axes[0].plot(survival.years, 100*survival.survival, marker='o', color='#315b7d')
axes[0].set(xlabel='Maturity (years)', ylabel='Risk-neutral survival (%)', title='Calibrated survival')
axes[1].bar(['Pay premium','Receive protection'], [-premium,protection], color=['#bc6c25','#315b7d'])
axes[1].axhline(0,color='#555555',lw=.8)
axes[1].set(ylabel='Present value per 100', title='Off-market protection-buyer ticket')
fig.tight_layout(); plt.show()
""",
    "conclusion": "The spread helpers reprice, survival is valid, and independently summed midpoint cash flows reproduce QuantLib's two legs and total PV. The ticket's fair spread belongs to its stated contract conventions; it is not automatically the five-year helper quote.",
    "kind": "Illustrative QuantLib desk workflow",
}

ADDITIONAL_TOPICS = [
    {
        "slug": "12-quotes-handles-risk",
        "title": "Quotes, handles and scenario risk",
        "teaser": "Update a market quote, relink a curve and revalue the same bond without rebuilding its contract.",
        "body": r"""A trader changes a rate and expects every dependent instrument to update. QuantLib's observable quotes and handles connect that workflow: `SimpleQuote` supplies a rate, `FlatForward` observes it, `RelinkableYieldTermStructureHandle` identifies the curve, and `DiscountingBondEngine` values the contract.

The example fixes a two-year zero-coupon bond, face 100 and zero settlement days. Its flat continuously compounded rate starts at 3.5% with Actual/365 Fixed. Quote shocks change the same live bond's value. The notebook compares each result against $100e^{-rT}$, checks signed zero-rate DV01 against $-T PV\times10^{-4}$, restores the quote after the sweep, and relinks the handle to an independently created 4.5% curve before restoring the original link.

The scenario object is the continuously compounded flat zero rate, not an OIS market-quote strip. That distinction determines what the reported sensitivity means. The [bond-risk chapter](../05-bond-risk/README.md) supplies quote-bucket risk with complete curve rebuilds. Fixed reference dates make these instantaneous scenarios: no carry, roll-down or settlement-date movement is included.

Both quote restoration and handle restoration are checked. This is useful for avoiding one scenario contaminating the next, but it does not model a production market-data feed. See [QuantLib handles](https://github.com/lballabio/QuantLib/blob/master/ql/handle.hpp) and [simple quotes](https://github.com/lballabio/QuantLib/blob/master/ql/quotes/simplequote.hpp).""",
        "calculation": r"""
with valuation_date():
    day_count = ql.Actual365Fixed()
    rate_quote = ql.SimpleQuote(.035)
    original_curve = ql.FlatForward(DATE, ql.QuoteHandle(rate_quote), day_count)
    handle = ql.RelinkableYieldTermStructureHandle(original_curve)
    maturity = CAL.advance(DATE, ql.Period('2Y'))
    bond = ql.ZeroCouponBond(0, CAL, 100., maturity, ql.ModifiedFollowing, 100., DATE)
    bond.setPricingEngine(ql.DiscountingBondEngine(handle))
    time = day_count.yearFraction(DATE, bond.maturityDate())
    base_rate, base_pv = rate_quote.value(), bond.NPV()
    rows = []
    try:
        for shock_bp in [-100, -50, 0, 50, 100]:
            rate_quote.setValue(base_rate+shock_bp*1e-4)
            expected = 100*np.exp(-rate_quote.value()*time)
            assert abs(bond.NPV()-expected) < 1e-10
            rows.append({'zero_rate_shock_bp':shock_bp, 'same_bond_PV':bond.NPV(),
                         'analytic_PV':expected, 'scenario_PnL':bond.NPV()-base_pv})
        rate_quote.setValue(base_rate+1e-4); up = bond.NPV()
        rate_quote.setValue(base_rate-1e-4); down = bond.NPV()
        signed_dv01 = (up-down)/2
        assert abs(signed_dv01-(-time*base_pv*1e-4)) < 1e-8
    finally:
        rate_quote.setValue(base_rate)
    assert abs(bond.NPV()-base_pv) < 1e-12
    alternate_curve = ql.FlatForward(DATE, .045, day_count)
    try:
        handle.linkTo(alternate_curve)
        relinked_pv = bond.NPV()
        assert abs(relinked_pv-100*np.exp(-.045*time)) < 1e-10
    finally:
        handle.linkTo(original_curve)
    assert abs(bond.NPV()-base_pv) < 1e-12
    scenarios = pd.DataFrame(rows)
    print(f'Signed flat-zero DV01: {signed_dv01:.8f} currency/bp per 100 face')
    print(f'Relinked 4.5% curve PV: {relinked_pv:.6f}; restored base PV: {bond.NPV():.6f}')
display(scenarios.round(6))
""",
        "figure": r"""
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(scenarios.zero_rate_shock_bp, scenarios.scenario_PnL, marker='o', label='Full revaluation', color='#315b7d')
ax.plot(scenarios.zero_rate_shock_bp, scenarios.zero_rate_shock_bp*signed_dv01,
        ls='--', label='First-order zero-rate DV01', color='#bc6c25')
ax.set(xlabel='Flat continuous zero-rate shock (bp)', ylabel='P&L per 100 face',
       title='One bond, observable quote updates')
ax.legend(); fig.tight_layout(); plt.show()
""",
        "conclusion": "Quote updates and curve relinking both propagate to the existing instrument. Every scenario matches direct discounting, the finite-difference sensitivity matches the derivative, and the original quote and link are restored.",
        "kind": "Illustrative QuantLib desk workflow",
    },
    {
        "slug": "13-caps-and-floors",
        "title": "Caps, floors and optionlet risk",
        "teaser": "Build a floating leg, price its cap and floor with Black, and reconstruct the optionlet values.",
        "body": r"""A floating-rate borrower can buy a cap to limit interest above a strike; a floor pays when the fixing falls below its strike. QuantLib represents both contracts on a dated `IborLeg`, with projection inherited from its index and discounting supplied by the pricing engine.

The notebook starts a three-year quarterly leg six months after the reference date, notional 100, Actual/360, Modified Following and zero fixing lag. It uses the illustrative dual curves, strike 4%, a flat Black optionlet volatility of 20%, and `BlackCapFloorEngine`. All reset dates are future dates. Indexed coupons are explicit so adjusted accrual periods are not silently substituted for index periods.

For each coupon, the code reads its fixing, value, maturity and payment dates, independently derives its index forward from projection discount factors, and reconstructs the Black caplet/floorlet value using the actual coupon accrual and OIS payment discount. The sum must match each QuantLib instrument. Cap minus floor must equal the discounted floating-minus-fixed coupons. A quote-based volatility sweep then shows the premium response while the contract and curves remain fixed.

Flat optionlet volatility is a constructed assumption, not a cap-volatility surface stripped from quotes. Unshifted Black requires positive forwards and strikes; normal or shifted-lognormal models need separately specified units and conventions. No smile calibration or hedge P&L is claimed. References: [caps and floors API](https://quantlib-python-docs.readthedocs.io/en/latest/instruments/caps.html) and [Black cap/floor engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/capfloor/blackcapfloorengine.cpp).""",
        "calculation": r"""
from scipy.stats import norm
with valuation_date():
    discount, projection, _ = curves()
    dh = ql.YieldTermStructureHandle(discount)
    index = ql.IborIndex('IllustrativeCap3M', ql.Period('3M'), 0, ql.USDCurrency(),
                        CAL, ql.ModifiedFollowing, False, ql.Actual360(),
                        ql.YieldTermStructureHandle(projection))
    start = CAL.advance(DATE, ql.Period('6M'))
    end = CAL.advance(start, ql.Period('3Y'))
    schedule = ql.Schedule(start, end, ql.Period('3M'), CAL, ql.ModifiedFollowing,
                           ql.ModifiedFollowing, ql.DateGeneration.Forward, False)
    leg = ql.IborLeg([100.], schedule, index, ql.Actual360(), ql.ModifiedFollowing,
                    withIndexedCoupons=True)
    strike, vol_quote = .04, ql.SimpleQuote(.20)
    engine = ql.BlackCapFloorEngine(dh, ql.QuoteHandle(vol_quote), ql.Actual365Fixed())
    cap, floor = ql.Cap(leg, [strike]), ql.Floor(leg, [strike])
    cap.setPricingEngine(engine); floor.setPricingEngine(engine)
    rows = []
    for flow in leg:
        coupon = ql.as_floating_rate_coupon(flow)
        fixing = coupon.fixingDate()
        value = index.valueDate(fixing); maturity = index.maturityDate(value)
        index_tau = index.dayCounter().yearFraction(value, maturity)
        forward = (projection.discount(value)/projection.discount(maturity)-1)/index_tau
        expiry = ql.Actual365Fixed().yearFraction(DATE, fixing)
        stddev = vol_quote.value()*np.sqrt(expiry)
        d1 = np.log(forward/strike)/stddev + stddev/2
        d2 = d1-stddev
        scale = coupon.nominal()*coupon.accrualPeriod()*discount.discount(coupon.date())
        caplet = scale*(forward*norm.cdf(d1)-strike*norm.cdf(d2))
        floorlet = scale*(strike*norm.cdf(-d2)-forward*norm.cdf(-d1))
        assert abs(forward-coupon.indexFixing()) < 1e-12
        rows.append({'payment':coupon.date().ISO(), 'forward_pct':forward*100,
                     'caplet_PV':caplet, 'floorlet_PV':floorlet,
                     'linear_coupon_PV':scale*(forward-strike)})
    optionlets = pd.DataFrame(rows)
    assert abs(optionlets.caplet_PV.sum()-cap.NPV()) < 1e-10
    assert abs(optionlets.floorlet_PV.sum()-floor.NPV()) < 1e-10
    assert abs(cap.NPV()-floor.NPV()-optionlets.linear_coupon_PV.sum()) < 1e-10
    values = []
    try:
        for vol in [.05, .10, .20, .30, .40]:
            vol_quote.setValue(vol)
            values.append({'Black_vol_pct':vol*100, 'cap_PV':cap.NPV(), 'floor_PV':floor.NPV()})
    finally:
        vol_quote.setValue(.20)
    volatility = pd.DataFrame(values)
    assert (np.diff(volatility.cap_PV) > 0).all()
    assert (np.diff(volatility.floor_PV) > 0).all()
    assert np.allclose(volatility.cap_PV-volatility.floor_PV,
                       optionlets.linear_coupon_PV.sum(), rtol=0, atol=1e-10)
    print(f'Base cap PV {cap.NPV():.6f}; floor PV {floor.NPV():.6f}; per 100 notional')
display(optionlets.round(6)); display(volatility.round(6))
""",
        "figure": r"""
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(volatility.Black_vol_pct, volatility.cap_PV, marker='o', label='Cap', color='#315b7d')
ax.plot(volatility.Black_vol_pct, volatility.floor_PV, marker='o', label='Floor', color='#bc6c25')
ax.set(xlabel='Flat Black optionlet volatility (%)', ylabel='Premium per 100 notional',
       title='Fixed contracts, changing optionlet volatility')
ax.legend(); fig.tight_layout(); plt.show()
""",
        "conclusion": "Independent optionlet sums reproduce both prices, and cap–floor parity reconciles to the linear floating-minus-fixed leg. Raising the assumed volatility increases both premiums while leaving their difference unchanged.",
        "kind": "Illustrative QuantLib desk workflow",
    },
    {
        "slug": "14-european-swaptions",
        "title": "European swaptions and annuity pricing",
        "teaser": "Construct a forward swap and price the right to pay or receive fixed using its discounted annuity.",
        "body": r"""A payer swaption gives the right to enter a payer swap at a fixed coupon; a receiver swaption gives the opposite right. Its underlying is a forward-starting swap, so the option price depends on the forward par rate and the discounted fixed-leg annuity, not on one bond yield.

The example uses one-year European exercise into a five-year USD swap with annual fixed and quarterly synthetic term-floating payments. Notional is 100, accrual is Actual/360, dates are Modified Following, fixing lag is zero, and the core illustrative projection and OIS discount curves remain distinct. `VanillaSwap`, `EuropeanExercise`, `Swaption` and `BlackSwaptionEngine` make the full contract-to-engine path visible. Settlement is physical; there is no cash-annuity convention to infer.

For annuity $A=N\sum_i\alpha_iD_i$, forward swap rate $F$, strike $K$ and expiry $T$, the payer price is $A[F\Phi(d_1)-K\Phi(d_2)]$, with $d_1=\log(F/K)/(\sigma\sqrt T)+\sigma\sqrt T/2$. The notebook reconstructs the annuity from fixed coupons, checks the forward swap PV against $A(F-K)$, compares QuantLib to a direct Black calculation, and verifies payer–receiver parity at three strikes. A quote update reprices the same at-the-money contract at several volatilities.

The 20% input is a flat lognormal swap-rate volatility, not 20 basis points of normal volatility. Positive rates are required by this unshifted Black example. No smile, volatility-surface calibration, Bermudan exercise or dynamic hedging is claimed. See [QuantLib swaption engines](https://quantlib-python-docs.readthedocs.io/en/latest/pricing_engines/swaptions.html) and the [Black engine implementation](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/swaption/blackswaptionengine.hpp).""",
        "calculation": r"""
from scipy.stats import norm
with valuation_date():
    discount, projection, _ = curves()
    dh = ql.YieldTermStructureHandle(discount)
    index = ql.IborIndex('IllustrativeSwaption3M', ql.Period('3M'), 0, ql.USDCurrency(),
                        CAL, ql.ModifiedFollowing, False, ql.Actual360(),
                        ql.YieldTermStructureHandle(projection))
    exercise_date = CAL.advance(DATE, ql.Period('1Y'))
    maturity = CAL.advance(exercise_date, ql.Period('5Y'))
    def schedule(tenor):
        return ql.Schedule(exercise_date, maturity, ql.Period(tenor), CAL,
                           ql.ModifiedFollowing, ql.ModifiedFollowing,
                           ql.DateGeneration.Forward, False)
    fixed, floating = schedule('1Y'), schedule('3M')
    def underlying(side, strike):
        swap = ql.VanillaSwap(side, 100., fixed, strike, ql.Actual360(),
                             floating, index, 0., ql.Actual360(), ql.ModifiedFollowing, True)
        swap.setPricingEngine(ql.DiscountingSwapEngine(dh))
        return swap
    probe = underlying(ql.VanillaSwap.Payer, .04)
    forward = probe.fairRate()
    annuity = sum(100*ql.as_coupon(c).accrualPeriod()*discount.discount(c.date())
                  for c in probe.fixedLeg())
    assert abs(annuity-abs(probe.fixedLegBPS())/1e-4) < 1e-10
    vol_quote = ql.SimpleQuote(.20)
    engine = ql.BlackSwaptionEngine(dh, ql.QuoteHandle(vol_quote), ql.Actual365Fixed())
    expiry = ql.Actual365Fixed().yearFraction(DATE, exercise_date)
    def option(side, strike):
        instrument = ql.Swaption(underlying(side, strike), ql.EuropeanExercise(exercise_date),
                                ql.Settlement.Physical)
        instrument.setPricingEngine(engine)
        return instrument
    rows = []
    for strike in [forward-.005, forward, forward+.005]:
        payer = option(ql.VanillaSwap.Payer, strike)
        receiver = option(ql.VanillaSwap.Receiver, strike)
        stddev = vol_quote.value()*np.sqrt(expiry)
        d1 = np.log(forward/strike)/stddev+stddev/2; d2 = d1-stddev
        manual = annuity*(forward*norm.cdf(d1)-strike*norm.cdf(d2))
        linear_pv = annuity*(forward-strike)
        assert abs(payer.NPV()-manual) < 1e-10
        assert abs(payer.NPV()-receiver.NPV()-linear_pv) < 1e-10
        assert abs(underlying(ql.VanillaSwap.Payer,strike).NPV()-linear_pv) < 1e-10
        rows.append({'strike_pct':strike*100, 'payer_PV':payer.NPV(),
                     'receiver_PV':receiver.NPV(), 'manual_payer_PV':manual,
                     'payer_minus_receiver':payer.NPV()-receiver.NPV()})
    prices = pd.DataFrame(rows)
    atm = option(ql.VanillaSwap.Payer, forward)
    values = []
    try:
        for vol in [.05, .10, .20, .30, .40]:
            vol_quote.setValue(vol)
            values.append({'Black_vol_pct':vol*100, 'ATM_payer_PV':atm.NPV()})
    finally:
        vol_quote.setValue(.20)
    volatility = pd.DataFrame(values)
    assert (np.diff(volatility.ATM_payer_PV) > 0).all()
    print(f'Forward par rate {100*forward:.6f}%; discounted annuity per 100 {annuity:.6f}')
display(prices.round(6)); display(volatility.round(6))
""",
        "figure": r"""
fig, axes = plt.subplots(1,2,figsize=(10,4))
axes[0].plot(prices.strike_pct, prices.payer_PV, marker='o', label='Payer', color='#315b7d')
axes[0].plot(prices.strike_pct, prices.receiver_PV, marker='o', label='Receiver', color='#bc6c25')
axes[0].set(xlabel='Frozen strike (%)', ylabel='Premium per 100', title='Exercise direction and strike')
axes[0].legend()
axes[1].plot(volatility.Black_vol_pct, volatility.ATM_payer_PV, marker='o', color='#315b7d')
axes[1].set(xlabel='Black swap-rate volatility (%)', ylabel='ATM premium per 100', title='Same ATM contract, updated volatility')
fig.tight_layout(); plt.show()
""",
        "conclusion": "The discounted annuity and forward rate reproduce QuantLib's European price. Payer–receiver parity equals the forward swap value, and volatility quote changes propagate to the same option contract.",
        "kind": "Illustrative QuantLib desk workflow",
    },
]
