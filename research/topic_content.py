"""Authored narratives and visible notebook calculations; original illustrative inputs."""

from research.desk_content import ADDITIONAL_TOPICS, CDS, FRA

TOPICS = [
    {
        "slug": "01-bsm-options",
        "title": "Black–Scholes–Merton options",
        "teaser": "How volatility, moneyness and dividends shape European option values.",
        "body": r"""A European call separates upside participation from ownership of the underlying. The question here is how much that convex payoff is worth when volatility, financing and dividends are specified, and which input drives a local hedge.

For spot $S$, strike $K$, maturity $T$, continuous rates $r,q$ and volatility $\sigma$,

$$C=Se^{-qT}\Phi(d_1)-Ke^{-rT}\Phi(d_2),\qquad d_1=\frac{\log(S/K)+(r-q+\sigma^2/2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T.$$

The exercise fixes $S=K=100$, $T=1$, $r=4\%$, $q=1\%$ and $\sigma=20\%$. A direct normal-distribution formula is compared with QuantLib's analytic European engine; call–put parity and a finite-difference delta provide separate checks. A volatility sweep shows the economic role of convexity.

Delta is measured per unit of spot. Vega describes a change in volatility, so a one-percentage-point volatility move is 0.01 in the formula's decimal units. These are model sensitivities under a constant-volatility diffusion; they do not estimate implied volatility, realized hedge costs, jump risk or a volatility smile. The contract is European and pays a continuous dividend yield; discrete dividends and American exercise need other models.

[QuantLib's analytic engine](https://github.com/lballabio/QuantLib/blob/master/ql/pricingengines/vanilla/analyticeuropeanengine.cpp) is the implementation reference; all numerical inputs are original illustrative assumptions.""",
        "calculation": r"""
from scipy.stats import norm
S, K, T, r, q, sigma = 100.0, 100.0, 1.0, .04, .01, .20
def call_price(spot, vol):
    d1 = (np.log(spot / K) + (r-q+vol**2/2)*T)/(vol*np.sqrt(T))
    d2 = d1-vol*np.sqrt(T)
    return spot*np.exp(-q*T)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
call = call_price(S, sigma)
d1 = (np.log(S/K)+(r-q+sigma**2/2)*T)/(sigma*np.sqrt(T))
d2 = d1-sigma*np.sqrt(T)
put = K*np.exp(-r*T)*norm.cdf(-d2)-S*np.exp(-q*T)*norm.cdf(-d1)
with valuation_date():
    dc = ql.Actual365Fixed()
    process = ql.BlackScholesMertonProcess(
        ql.QuoteHandle(ql.SimpleQuote(S)),
        ql.YieldTermStructureHandle(ql.FlatForward(DATE, q, dc)),
        ql.YieldTermStructureHandle(ql.FlatForward(DATE, r, dc)),
        ql.BlackVolTermStructureHandle(ql.BlackConstantVol(DATE, ql.NullCalendar(), sigma, dc)))
    option = ql.VanillaOption(ql.PlainVanillaPayoff(ql.Option.Call, K), ql.EuropeanExercise(DATE+365))
    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    ql_price, ql_delta = option.NPV(), option.delta()
finite_delta = (call_price(S+.001, sigma)-call_price(S-.001, sigma))/.002
assert abs(call-ql_price) < 1e-10
assert abs(call-put-(S*np.exp(-q*T)-K*np.exp(-r*T))) < 1e-10
assert abs(finite_delta-ql_delta) < 1e-7
display(pd.DataFrame([{'call_formula':call, 'call_QuantLib':ql_price, 'put':put, 'delta':ql_delta, 'finite_difference_delta':finite_delta}]))
""",
        "figure": r"""
vols = np.linspace(.05, .50, 60)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(100*vols, [call_price(S,v) for v in vols], color='#315b7d')
ax.scatter([100*sigma],[call],color='#bc6c25',label='Base assumption')
ax.set(xlabel='Assumed annual volatility (%)', ylabel='Call value per option', title='European call value and volatility')
ax.legend(); fig.tight_layout(); plt.show()
""",
        "conclusion": "The formula, QuantLib price and parity agree. The increasing value across the volatility sweep reflects the convex call payoff under this model; it is not an empirical volatility premium.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "02-yield-curves",
        "title": "Yield curves and discount factors",
        "teaser": "Turn par quotes into dated discount factors and forward rates.",
        "body": r"""A quoted par rate, a zero rate and a forward rate answer different questions. A par rate makes a specified coupon instrument worth par; a discount factor prices one unit paid at a future date; a forward rate prices the exchange between two future dates.

For continuously compounded zero rates, $D(0,t)=e^{-z(t)t}$. With a declared simple accrual $\tau$, the discount-implied forward is $F(t_1,t_2)=[D(0,t_1)/D(0,t_2)-1]/\tau$. These transformations must use compatible dates and day counts.

This chapter bootstraps the versioned 1–10-year illustrative OIS par strip using explicit calendar and coupon conventions. It displays input quotes beside the zero and forward rates produced by the curve. Each helper must reprice its input within $10^{-8}$ in decimal rate units. The plot makes clear why a par quote should not be inserted directly as a zero rate.

The curve uses log-linear discount interpolation and Actual/365 Fixed zero-rate reporting. The forward-rate table uses Actual/360 accruals between adjusted annual dates. Only maturities covered by the fixture are used. Positive discount factors are required; monotonic decline is not imposed as a universal condition because negative-rate environments can imply discount factors above one.

These are constructed rates dated 15 September 2026. This chapter studies internal curve consistency; no daily Treasury series, live SOFR term surface or executable quote set is being reproduced. See the [core conventions](../../docs/01-methods.md) for the exact instrument definitions.""",
        "calculation": r"""
with valuation_date():
    d, p, residuals = curves()
    quotes = fixture()
    rows=[]
    dates=[CAL.advance(DATE, ql.Period(y, ql.Years)) for y in range(1,11)]
    for y, date in enumerate(dates,1):
        t=ql.Actual365Fixed().yearFraction(DATE,date)
        start = DATE if y == 1 else dates[y-2]
        tau=ql.Actual360().yearFraction(start,date)
        rows.append({'years':y,'discount_factor':d.discount(date),'zero_rate_pct':-100*np.log(d.discount(date))/t,'annual_forward_pct':100*(d.discount(start)/d.discount(date)-1)/tau})
    curve_table=pd.DataFrame(rows).assign(par_quote_pct=100*quotes.ois_rate)
assert residuals.residual.abs().max() < 1e-8
assert (curve_table.discount_factor > 0).all()
display(curve_table.round(6))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(7,4))
for col,label,color in [('par_quote_pct','OIS par quote','#315b7d'),('zero_rate_pct','Continuous zero','#bc6c25'),('annual_forward_pct','One-year simple forward','#718355')]:
    ax.plot(curve_table.years,curve_table[col],marker='o',label=label,color=color)
ax.set(xlabel='Maturity (years)',ylabel='Annual rate (%)',title='Par, zero and forward rates: different objects')
ax.legend();fig.tight_layout();plt.show()
""",
        "conclusion": "The same calibrated curve produces distinct par, zero and forward rates. Small repricing errors establish consistency with the declared inputs, not the accuracy of those inputs as market observations.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "03-curve-inversion",
        "title": "Yield-curve inversion",
        "teaser": "Separate a negative term spread from a recession forecast.",
        "body": r"""An inversion is a statement about the ordering of yields across maturities. A 10Y minus 2Y spread below zero says the selected long rate is below the selected short rate; it does not identify why that shape arose or forecast the date of a recession on its own.

This chapter calculates the spread from the constructed curve in two ways: directly from 10Y and 2Y OIS par quotes, and from the bootstrapped continuously compounded zero rates. It then applies a parallel shift and opposite steepener/flattener shocks to the zero-rate nodes. Reporting the object being shocked avoids mixing a par-quote spread with a zero-rate spread.

The spread is $10^4[z(10)-z(2)]$ basis points. A parallel shift cancels exactly. A shape shock changes the spread according to the difference between the long- and short-node shocks. This simple identity is checked in the notebook, while the figure compares the entire constructed zero curve rather than only two points.

Scenario nodes are deterministic illustrations, not historical observations or newly calibrated par instruments. The exercise does not estimate recession probabilities, term premia, policy expectations or the profitability of a curve trade. A historical prediction study would need a dated public yield series, a defined target and forecast horizon, release-vintage treatment and a genuinely later evaluation period. Those are distinct research questions from measuring an inversion.""",
        "calculation": r"""
with valuation_date():
    d,_,_=curves()
    years=np.arange(1,11)
    dates=[CAL.advance(DATE,ql.Period(int(y),ql.Years)) for y in years]
    z=np.array([-np.log(d.discount(date))/ql.Actual365Fixed().yearFraction(DATE,date) for date in dates])
scenarios={'Base':z,'Parallel +100 bp':z+.01,'Steepener':z+np.linspace(-.005,.005,10),'Flattener':z+np.linspace(.005,-.005,10)}
spreads=pd.DataFrame([{'scenario':name,'10Y_minus_2Y_zero_bp':1e4*(values[9]-values[1])} for name,values in scenarios.items()])
assert abs(spreads.iloc[0,1]-spreads.iloc[1,1]) < 1e-10
for name, direction in [('Steepener', 1), ('Flattener', -1)]:
    shifted = scenarios[name]
    node_shocks = shifted-z
    spread_change = (shifted[9]-shifted[1])-(z[9]-z[1])
    assert abs(spread_change-(node_shocks[9]-node_shocks[1])) < 1e-12
    # Across 2Y to 10Y, eight of the nine equal tenor steps span 100 bp.
    assert abs(1e4*spread_change-direction*(8/9)*100) < 1e-10
par=fixture().set_index('years').ois_rate
print(f'Constructed par-quote 10Y–2Y spread: {(par.loc[10]-par.loc[2])*1e4:.2f} bp')
display(spreads.round(4))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(7,4))
for (name,values),color in zip(scenarios.items(),['#315b7d','#777777','#bc6c25','#718355']):
    ax.plot(years,100*values,label=name,color=color)
ax.set(xlabel='Maturity (years)',ylabel='Continuous zero rate (%)',title='Constructed curve shapes and inversion')
ax.legend();fig.tight_layout();plt.show()
""",
        "conclusion": "The parallel shock changes the level but leaves the term spread unchanged. Steepening and flattening change the spread by construction; none of these scenarios supplies recession evidence.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "04-bond-valuation",
        "title": "Bond valuation and accrued interest",
        "teaser": "Trace a bond price to coupons, principal, day counts and discounting.",
        "body": r"""A bond price becomes inspectable when every remaining payment has a date, amount and discount factor. The dirty price is the present value of those payments; the clean price removes accrued interest under the contract's accrual convention.

$$P_{dirty}=\sum_i CF_iD(0,t_i),\qquad P_{clean}=P_{dirty}-AI.$$

The case is a synthetic USD 100-face bond paying 4% annually in semiannual installments, issued in March 2026 and maturing in September 2033. The primary day count is Actual/Actual ISMA. The notebook reconstructs the dated cash flows independently and reconciles their discounted sum with QuantLib at 15 September 2026. A second valuation one month later uses a newly anchored flat 3.5% curve solely to expose nonzero accrued interest and verify the clean/dirty identity.

The second date is a separate convention exercise, not a holding-period P&L or a forecast of curve evolution. On each date, past/reference-date payments are excluded consistently. Zero settlement days keeps the independent PV and the engine on the same date; production settlement rules require corresponding treatment.

There is no credit, liquidity, tax or embedded-option spread. The price is therefore conditional on the supplied discount curve and synthetic contract, not a valuation of a quoted Treasury CUSIP or corporate bond. The risk chapter builds on the same cash-flow view to distinguish a yield derivative from a rebuilt-curve quote sensitivity.""",
        "calculation": r"""
from research.pricing import bond
with valuation_date():
    d,_,_=curves()
    instrument,flows=bond(d)
    primary={'date':DATE.ISO(),'clean':instrument.cleanPrice(),'accrued':instrument.accruedAmount(),'dirty':instrument.dirtyPrice(),'PV':instrument.NPV()}
    assert abs(flows.pv.sum()-instrument.NPV()) < 1e-8
later=ql.Date(15,10,2026)
with valuation_date(later):
    shifted=ql.FlatForward(later,.035,ql.Actual365Fixed())
    instrument,_=bond(shifted)
    followup={'date':later.ISO(),'clean':instrument.cleanPrice(),'accrued':instrument.accruedAmount(),'dirty':instrument.dirtyPrice(),'PV':instrument.NPV()}
    independent=sum(cf.amount()*shifted.discount(cf.date()) for cf in instrument.cashflows() if cf.date()>later)
    assert abs(independent-instrument.NPV()) < 1e-8
prices=pd.DataFrame([primary,followup])
assert np.allclose(prices.clean+prices.accrued,prices.dirty,atol=1e-10)
assert followup['accrued'] > 0
display(prices.round(6));display(flows.round(6))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(8,4))
ax.bar(flows.date,flows.pv,color='#315b7d')
ax.set(xlabel='Payment date',ylabel='Present value per 100 face',title='Primary bond: where present value comes from')
ax.tick_params(axis='x',rotation=60);fig.tight_layout();plt.show()
""",
        "conclusion": "The cash-flow sum matches the engine. Accrued interest is zero on the primary coupon date and positive in the separate October convention example; clean and dirty prices reconcile on both dates.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "05-bond-risk",
        "title": "Bond Greeks, curve risk and hedging",
        "teaser": "See what duration removes, what convexity adds and what a one-swap hedge leaves.",
        "body": r"""“DV01” is incomplete without the variable that moves. A parallel yield bump, a continuous zero spread and a parallel shift to bootstrapped market quotes can produce different sensitivities because they change different objects.

The connected study defines signed quote DV01 as $[P(q+1bp)-P(q-1bp)]/2$, in currency per positive basis point. It rebuilds discount and projection curves for each bump. Bond DV01 is negative with this convention. Separate quote buckets reveal the term-structure directions hidden in one parallel number.

The notebook independently differentiates discounted bond cash flows with respect to a continuous zero spread: $-10^{-4}\sum_i t_iCF_iD_i$. A central difference checks that derivative. It then reads the primary study's frozen hedge and scenario revaluations, verifying $\Delta P_{hedged}=\Delta P_{bond}+h\Delta P_{swap}$. The companion figure compares exact residuals with a bucket approximation across parallel, slope and local-tenor shocks.

The hedge ratio $h=-DV01_{bond}/DV01_{swap}$ removes one first-order direction at inception. It does not cancel every tenor bucket, the separate projection exposure, or all second-order effects. All shocks are instantaneous, with coupon and positions frozen. Carry, roll-down, trade costs and rebalancing are outside this experiment.

[The full study](../../study.ipynb) retains the calibrated inputs, bump-size checks and convention alternatives needed to interpret these residuals.""",
        "calculation": r"""
flows=pd.read_csv(RESULTS/'cashflows.csv').query('instrument=="bond"').copy()
t=np.array([ql.Actual365Fixed().yearFraction(DATE,ql.DateParser.parseISO(x)) for x in flows.date])
analytic=-1e-4*np.sum(t*flows.pv)
h=.000001
central=np.sum(flows.pv*(np.exp(-h*t)-np.exp(h*t)))/(2*h)*1e-4
assert abs(analytic-central)<1e-8
pnl=pd.read_csv(RESULTS/'scenario_pnl.csv')
hedge=pd.read_csv(RESULTS/'hedge.csv').iloc[0].swap_units
assert np.allclose(pnl.hedged_pnl,pnl.unhedged_bond_pnl+hedge*pnl.swap_pnl_per100,atol=1e-12)
display(pd.DataFrame([{'zero_spread_analytic_DV01':analytic,'zero_spread_central_DV01':central,'swap_units_per_100_bond':hedge}]))
display(pnl.round(6))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(8,4))
pnl.set_index('scenario')[['hedged_pnl','bucket_first_order']].rename(columns={'hedged_pnl':'Exact hedge P&L','bucket_first_order':'Bucket approximation'}, index={'local_7y':'Local 7Y +100 bp','flattener':'Flattener','steepener':'Steepener','parallel_down100':'Parallel −100 bp','parallel_up100':'Parallel +100 bp'}).plot.barh(ax=ax,color=['#315b7d','#bc6c25'])
ax.axvline(0,color='#555555',lw=.8)
ax.set(xlabel='USD P&L per 100 bond',ylabel='',title='Frozen one-swap hedge: residual curve risk')
fig.tight_layout();plt.show()
""",
        "conclusion": "The independent zero-spread derivative agrees with its finite difference. The frozen swap removes most parallel sensitivity, while the local 7Y and slope shocks expose residual curve risk. Zero-spread DV01 and quote DV01 remain different measures.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "06-swap-curves",
        "title": "Swap curves: projection and discounting",
        "teaser": "Separate the curve forecasting floating coupons from the curve discounting payments.",
        "body": r"""A floating coupon forecast and the present value of that coupon serve different roles. This chapter asks what changes when a term-index projection curve is distinct from the collateral discount curve.

For a synthetic term index, the projected simple rate is $L=[P^{proj}(t_a)/P^{proj}(t_b)-1]/\tau_{index}$. The coupon amount uses its actual contract accrual and is discounted with $D^{disc}(t_{pay})$. Index value/maturity dates can differ slightly from coupon accrual dates after holiday adjustments.

The fixture supplies OIS par quotes and an illustrative term swap strip 50 basis points above it. QuantLib first bootstraps the OIS discount curve, then builds the term projection curve while discounting its calibration helpers with OIS. The notebook checks both sets of helper residuals and values the same payer swap using dual curves and an OIS-only projection counterfactual. Its fixed coupon remains frozen across that comparison.

The synthetic USD 3M index is not current USD LIBOR. A constant 50-bp input difference is a teaching assumption, not a statement about observed credit or basis premia. The study does not calibrate a full collection of overnight, term, futures, basis and collateral instruments.

Calibration error measures the reproduction of input quotes. The single-curve valuation difference measures a controlled modeling choice. Neither is an observed market pricing error. See [IRS cash flows](../08-interest-rate-swaps/README.md) for the coupon-level reconciliation.""",
        "calculation": r"""
from research.pricing import swap
with valuation_date():
    discount,projection,residuals=curves()
    dual,_,coupon=swap(discount,projection)
    single,_,_=swap(discount,discount,coupon)
    comparison=pd.DataFrame([{'projection':'Separate term curve','fixed_coupon_pct':coupon*100,'payer_swap_PV':dual.NPV()},{'projection':'OIS-only counterfactual','fixed_coupon_pct':coupon*100,'payer_swap_PV':single.NPV()}])
    nodes=[]
    for y in range(1,11):
        date=CAL.advance(DATE,ql.Period(y,ql.Years))
        t=ql.Actual365Fixed().yearFraction(DATE,date)
        nodes.append({'years':y,'discount_zero_pct':-100*np.log(discount.discount(date))/t,'projection_zero_pct':-100*np.log(projection.discount(date))/t})
assert residuals.residual.abs().max()<1e-8
assert abs(comparison.iloc[0].payer_swap_PV)<1e-8
display(comparison.round(6));display(residuals.round(10))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(7,4))
pd.DataFrame(nodes).rename(columns={'discount_zero_pct':'Discount curve','projection_zero_pct':'Projection curve'}).plot(x='years',y=['Discount curve','Projection curve'],ax=ax,color=['#315b7d','#bc6c25'])
ax.set(xlabel='Maturity (years)',ylabel='Continuous zero rate (%)',title='Discount and projection curves from constructed quotes')
fig.tight_layout();plt.show()
""",
        "conclusion": "Both curves reproduce their own calibration instruments. Substituting the discount curve for term projection changes the swap PV while its contractual fixed coupon remains unchanged.",
        "kind": "Illustrative numerical exercise",
    },
    FRA,
    {
        "slug": "08-interest-rate-swaps",
        "title": "Interest rate swaps",
        "teaser": "Build a fixed-for-floating swap from its two legs and freeze it before hedging.",
        "body": r"""A payer interest rate swap exchanges fixed payments for floating receipts. The fair fixed coupon sets their initial present values equal; it is a property of the schedule, projection and discounting assumptions together.

Writing the fixed annuity as $A=\sum_i\alpha_iD_i$ and the projected floating value per unit notional as $B$, the fair rate is $K^*=B/A$. A swap with a frozen coupon $K$ has $PV=N(B-KA)$ from the payer's perspective.

The case starts one business day after 15 September 2026, lasts seven years, pays fixed annually and receives a synthetic USD 3M rate quarterly. It uses Actual/360, Modified Following and separate term projection/OIS discount curves. The next-business-day start avoids a hidden requirement for historical index fixings.

The notebook reconstructs each leg from indexed-coupon dates, computes the fair rate independently and compares the total PV with QuantLib. It then raises the fixed coupon by 10 bp and checks the analytical annuity effect. This holds the forecast curve and floating leg fixed, separating a contractual coupon change from a market-curve shock.

There is no principal exchange in this single-currency IRS. The seven-year payer becomes the hedge instrument in the connected bond study. When scenarios move curves, its coupon and hedge units stay frozen; recalculating a fair coupon after each shock would replace the original contract and erase the risk being studied.""",
        "calculation": r"""
from research.pricing import swap
with valuation_date():
    discount,projection,_=curves()
    instrument,flows,rate=swap(discount,projection)
    fixed=flows.query('instrument=="fixed"')
    floating=flows.query('instrument=="float"')
    annuity=np.sum(fixed.accrual*fixed.discount)
    independent_rate=floating.pv.sum()/(100*annuity)
    assert abs(independent_rate-rate)<1e-10
    assert abs(flows.pv.sum()-instrument.NPV())<1e-8
    offmarket,_,_=swap(discount,projection,rate+.001)
    assert abs(offmarket.NPV()+100*.001*annuity)<1e-8
    summary=pd.DataFrame([{'fair_fixed_rate_pct':100*rate,'fixed_annuity':annuity,'par_swap_PV':instrument.NPV(),'PV_after_fixed_coupon_plus10bp':offmarket.NPV()}])
display(summary.round(6));display(flows.round(6))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(7,4))
leg_pv=flows.groupby('instrument').pv.sum().reindex(['fixed','float'])
ax.bar(['Pay fixed','Receive floating'],leg_pv,color=['#bc6c25','#315b7d'])
ax.axhline(0,color='#555555',lw=.8)
ax.set(ylabel='Present value per 100 notional',title='At the fair coupon, swap leg values offset')
fig.tight_layout();plt.show()
""",
        "conclusion": "Independent floating cash flows and the fixed annuity reproduce the fair coupon. Paying an additional 10 bp reduces PV by exactly notional times the annuity times 0.001 under unchanged curves.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "09-fx-forwards",
        "title": "FX forwards and covered interest parity",
        "teaser": "Price a future currency exchange with dated domestic and foreign cash flows.",
        "body": r"""An FX forward fixes the exchange rate for a future currency exchange. To keep signs visible, spot and strike are quoted as USD per EUR, and the position receives one EUR and pays $K$ USD at maturity.

Under zero basis and compatible collateral assumptions,

$$F=S\frac{D_{EUR}}{D_{USD}},\qquad PV_{USD}=S D_{EUR}-K D_{USD}.$$

The exercise uses spot 1.10 USD/EUR, the constructed USD curve and an illustrative flat continuously compounded EUR rate of 2.5%. At the fair forward, discounted payments cancel. Strikes 0.01 below and above fair value expose the sign of a long-EUR forward. A one-to-ten-year table connects the interest-rate difference to forward points.

Forward points are quoted in $10^{-4}$ USD/EUR in this notebook, so a point equals 0.0001 in the outright exchange rate. The strike is not an expected future spot forecast: it is the rate implied by the chosen no-basis discount factors and replication assumptions.

The numerical parity identity does not establish an executable arbitrage. Observed forward prices can also reflect collateral, funding, balance-sheet costs, bid/ask and currency basis. Those inputs are not supplied here. The [BIS discussion of covered interest parity](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis) motivates treating zero basis as an assumption rather than an observed market fact.""",
        "calculation": r"""
from research.pricing import fx_forward
spot=1.10
with valuation_date():
    discount,_,_=curves()
    rows=[]
    for year in range(1,11):
        date=CAL.advance(DATE,ql.Period(year,ql.Years))
        t=ql.Actual365Fixed().yearFraction(DATE,date)
        usd,eur=discount.discount(date),np.exp(-.025*t)
        forward=fx_forward(spot,usd,eur)
        rows.append({'years':year,'USD_discount':usd,'EUR_discount':eur,'forward_USD_per_EUR':forward,'forward_points':(forward-spot)*1e4,'fair_PV':spot*eur-forward*usd})
fx=pd.DataFrame(rows)
assert fx.fair_PV.abs().max()<1e-12
base=fx.iloc[0]
strikes=pd.DataFrame([{'strike':base.forward_USD_per_EUR+b,'long_EUR_PV_USD':spot*base.EUR_discount-(base.forward_USD_per_EUR+b)*base.USD_discount} for b in [-.01,0,.01]])
assert strikes.iloc[0].long_EUR_PV_USD>0>strikes.iloc[2].long_EUR_PV_USD
display(fx.round(6));display(strikes.round(6))
""",
        "figure": r"""
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(fx.years,fx.forward_points,marker='o',color='#315b7d')
ax.set(xlabel='Maturity (years)',ylabel='Forward points (0.0001 USD/EUR)',title='No-basis forward points from illustrative curves')
fig.tight_layout();plt.show()
""",
        "conclusion": "All fair forwards have zero discounted PV under the stated no-basis assumptions. A lower agreed USD strike benefits a long-EUR forward; forward points are not a forecast of the future spot rate.",
        "kind": "Illustrative numerical exercise",
    },
    {
        "slug": "10-cross-currency-swaps",
        "title": "Cross-currency swaps",
        "teaser": "Track principal exchanges, coupon legs and the currency used to report value.",
        "body": r"""A cross-currency swap exchanges cash flows in two currencies. The principal exchanges matter alongside the coupons: dropping them changes the exposure being valued.

This deliberately simple case is a five-year, fixed-for-fixed swap. At inception the holder receives EUR 100 and pays USD 110 at spot 1.10 USD/EUR. During the swap the holder pays EUR coupons and receives USD coupons; at maturity the holder returns EUR 100 and receives USD 110. Each currency's coupon is set to its own par fixed-bond rate under the declared flat curve.

For currency $c$, annual accruals and discount factors $D_c(i)$ give $k_c=[1-D_c(T)]/\sum_iD_c(i)$. The remaining-leg USD value immediately after inception is $PV_{USD\ leg}-S\,PV_{EUR\ leg}$. At par inception both legs and the initial exchanges cancel. After inception, moving the conversion spot while holding the contractual coupons and curves fixed exposes the position's FX sensitivity.

The notebook explicitly lists the time-zero and final principal exchanges, checks par leg values, and compares a finite-difference spot derivative with $-PV_{EUR\ leg}$. A separate 10-bp change to the contractual EUR coupon shows the coupon-annuity effect; it is not a calibrated market basis spread.

Assumptions are flat continuous USD 4% and EUR 2.5%, deterministic rates, annual exact-year payments, zero basis and compatible collateral. This is neither a floating-versus-floating basis-swap engine nor a collateralized multi-currency curve bootstrap. Resettable notionals, currency-specific calendars, funding, collateral and observed basis quotes remain outside this chapter. [BIS](https://www.bis.org/publications/qr-201609/covered-interest-parity-lost-understanding-cross-currency-basis) provides the institutional context for that boundary.""",
        "calculation": r"""
spot,eur_notional=1.10,100.0
usd_notional=spot*eur_notional
times=np.arange(1,6,dtype=float)
dusd,deur=np.exp(-.04*times),np.exp(-.025*times)
kusd,keur=(1-dusd[-1])/dusd.sum(),(1-deur[-1])/deur.sum()
usd_cash=np.full(5,usd_notional*kusd);usd_cash[-1]+=usd_notional
eur_cash=np.full(5,eur_notional*keur);eur_cash[-1]+=eur_notional
pv_usd,pv_eur=np.dot(usd_cash,dusd),np.dot(eur_cash,deur)
assert abs(pv_usd-usd_notional)<1e-10 and abs(pv_eur-eur_notional)<1e-10
assert abs(pv_usd-spot*pv_eur)<1e-10
ledger=pd.DataFrame({'year':np.r_[0,times],'USD_received':np.r_[-usd_notional,usd_cash],'EUR_received':np.r_[eur_notional,-eur_cash]})
pv=lambda s:pv_usd-s*pv_eur
assert abs((pv(spot+.0001)-pv(spot-.0001))/.0002+pv_eur)<1e-8
extra_eur_coupon_pv=-spot*eur_notional*.001*deur.sum()
display(ledger.round(6))
display(pd.DataFrame([{'USD_coupon_pct':100*kusd,'EUR_coupon_pct':100*keur,'remaining_legs_PV_USD':pv(spot),'FX_delta_USD_per_USD_EUR':-pv_eur,'PV_of_EUR_coupon_plus10bp':extra_eur_coupon_pv}]))
""",
        "figure": r"""
spots=np.linspace(.90,1.30,60)
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(spots,[pv(s) for s in spots],color='#315b7d');ax.axhline(0,color='#555555',lw=.8)
ax.axvline(spot,color='#bc6c25',ls='--',label='Initial spot')
ax.set(xlabel='Scenario spot (USD/EUR)',ylabel='Remaining-leg value (USD)',title='Fixed-for-fixed swap: spot conversion risk after inception')
ax.legend();fig.tight_layout();plt.show()
""",
        "conclusion": "The two par legs and the initial principal exchange balance at inception. The remaining fixed cash flows still carry FX exposure; a zero initial value does not imply a risk-free position. No market currency basis is estimated.",
        "kind": "Illustrative numerical exercise",
    },
    CDS,
    *ADDITIONAL_TOPICS,
]
