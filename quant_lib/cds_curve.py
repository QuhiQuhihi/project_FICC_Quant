import os
import datetime
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import QuantLib as ql


def get_irs_quote(today):
    quote = pd.read_excel(os.path.join("/mnt/c/workspace/project_FICC_Quant/market_data/cds_data.xlsx"),index_col='Tenor',sheet_name='USDIRS')
    # pre-processing dataframe
    quote['DaysToMaturity'] = np.nan
    quote['Maturity'] = pd.to_datetime(quote['Maturity']).dt.date

    for tenor in quote.index:
        quote.loc[tenor, 'DaysToMaturity'] = (quote.loc[tenor, 'Maturity'] - today).days
    return quote

def get_cds_quote(today):
    quote = pd.read_excel(os.path.join("/mnt/c/workspace/project_FICC_Quant/market_data/cds_data.xlsx"),index_col='Tenor',sheet_name='ROKCDS')
    # pre-processing dataframe
    quote['DaysToMaturity'] = np.nan
    quote['Maturity'] = pd.to_datetime(quote['Maturity']).dt.date

    for tenor in quote.index:
        quote.loc[tenor, 'DaysToMaturity'] = (quote.loc[tenor, 'Maturity'] - today).days
    return quote

# construct IRS curve
def swap_curve(today, quote):

    # divide dataframe into 3 parts
    depo = quote[quote['InstType'] == 'CASH']
    futures = quote[quote['InstType'] == 'FUTURES']
    swap = quote[quote['InstType'] == 'SWAP']

    # Set evaluation date
    todays_date = ql.Date(today.day, today.month, today.year)
    ql.Settings.instance().evaluationDate = todays_date

    #Market Conventions
    calendar = ql.UnitedStates()
    dayCounter = ql.Actual360()
    convention = ql.ModifiedFollowing
    settlementDays = 2
    frequency = ql.Semiannual

    ### Build Rate Helper ###

    # 1_Deposit rate helper
    depositHelpers = [
        ql.DepositRateHelper(
            ql.QuoteHandle(ql.SimpleQuote(rate/100)),
            ql.Period(int(day), ql.Days),
            settlementDays,
            calendar,
            convention,
            False,
            dayCounter
        )
        for day, rate in zip(depo['DaysToMaturity'], depo['Market.Mid'])
    ]

    # 2_ Futures rate helper
    futuresHelpers = []
    for i, price in enumerate(futures['Market.Mid']):
        iborStartDate = ql.Date(
            futures['Maturity'][i].day,
            futures['Maturity'][i].month,
            futures['Maturity'][i].year
        )
        
        futuresHelpers = ql.FuturesRateHelper(
            ql.QuoteHandle(ql.SimpleQuote(price)),
            iborStartDate,
            3,
            calendar,
            convention,
            False,
            dayCounter
        )
        futuresHelpers.append(futuresHelpers)

    # 3_ Swap rate helper
    swapHelpers = [ql.SwapRateHelper(
        ql.QuoteHandle(ql.SimpleQuote(rate/100)),
        ql.Period(int(day), ql.Days),
        calendar,
        frequency,
        convention,
        dayCounter,
        ql.Euribor3M()
        )
        for day, rate in zip(swap['DaysToMaturity'], swap['Market.Mid'])
    ]

    # Combine 1_2_3 with Piece wise linear zero method
    # Curve construction
    helpers = depositHelpers + futuresHelpers + swapHelpers
    depoFuturesSwapCurve = ql.PiecewiseLinearZero(todays_date, helpers, dayCounter)

    return depoFuturesSwapCurve

def cds_curve(today, quote, discount_curve):
    # Set Evaluation Date
    todays_date = ql.Date(today.day, today.month, today.year)
    ql.Settings.instance().evaluationDate = todays_date

    # Tenor
    tenors = [
        ql.Period(6, ql.Months),
        ql.Period(1, ql.Years),
        ql.Period(2, ql.Years),
        ql.Period(3, ql.Years),
        ql.Period(4, ql.Years),
        ql.Period(5, ql.Years),
        ql.Period(7, ql.Years),
        ql.Period(10, ql.Years)
    ]

    # Market Conventions
    settlement_days = 2
    calendar = ql.UnitedStates()
    recovery_rate = 0.4
    frequency = ql.Quarterly
    convention = ql.ModifiedFollowing
    date_generation = ql.DateGeneration.CDS
    day_count = ql.Actual360()

    cdsHelpers = [
        ql.SpreadCdsHelper(ql.QuoteHandle(ql.SimpleQuote(spread/10000)),
        tenor,
        settlement_days,
        calendar,
        frequency,
        convention,
        date_generation,
        day_count,
        recovery_rate,
        ql.YieldTermStructureHandle(discount_curve)
        )
    for spread, tenor in zip(quote['Market.Mid'], tenors)]
    
    cds_curve = ql.PiecewiseFlatHazardRate(todays_date, cdsHelpers, day_count)

    return cds_curve

def default_prob(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    default_prob = curve.defaultProbability(date)
    return default_prob

def survival_prob(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    survival_prob = curve.survivalProbability(date)
    return survival_prob



if __name__ == "__main__":
    todays_date = datetime.date(2020,12,11)

    irs_quote = get_irs_quote(today=todays_date)
    cds_quote = get_cds_quote(today=todays_date)

    discount_curve = swap_curve(today=todays_date, quote=irs_quote)
    hazard_curve = cds_curve(today=todays_date, quote=cds_quote, discount_curve=discount_curve)

    cds_quote['default prob'] = np.nan
    cds_quote['survival prob'] = np.nan

    for tenor, date in zip(cds_quote.index, cds_quote['Maturity']):
        cds_quote.loc[tenor, 'default prob'] = default_prob(date, hazard_curve)
        cds_quote.loc[tenor, 'survival prob'] = survival_prob(date, hazard_curve)



    print(cds_quote[['default prob', 'survival prob']])

    # plot the result
    plt.figure(figsize=(16,8))
    plt.plot(cds_quote['default prob'], 'b-', label='Default Probability')
    plt.title('Default Probability', loc='center')
    plt.xlabel('maturity')
    plt.ylabel('%')


    # plot the result
    plt.figure(figsize=(16,8))
    plt.plot(cds_quote['survival prob'], 'g-', label='Survival Probability')
    plt.title('Survival Probability', loc='center')
    plt.xlabel('maturity')
    plt.ylabel('%')