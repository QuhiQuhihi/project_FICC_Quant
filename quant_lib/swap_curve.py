import os
import datetime
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import QuantLib as ql
import xlwings as xw


def get_quote(today):
    quote = pd.read_excel(os.path.join("/mnt/c/workspace/project_FICC_Quant/market_data/swap_data.xlsx"),index_col='Tenor')
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

# use curve to compute discount factor and zero rate
# the curve is calcualted with module used while pricing treasury
def discount_factor(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    return curve.discount(date)

def zero_rate(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    day_counter = ql.Actual360()
    compounding = ql.Compounded
    freq = ql.Continuous
    zero_rate = curve.zeroRate(
        date,
        day_counter,
        compounding,
        freq
    ).rate()

    return zero_rate

# cacualte forward rate
def forward_rate(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    day_counter = ql.Actual360()
    compounding = ql.Compounded
    freq = ql.Continuous
    forward_rate = curve.forwardRate(
        date,
        date,
        day_counter,
        compounding,
        freq,
        True
    ).rate()
    
    return forward_rate


if __name__ == "__main__":
    today = datetime.date(2020,10,9)
    quote = get_quote(today=today)
    curve = swap_curve(today=today, quote=quote)

    # calculate discount factor/ zero rate/ forward rate
    quote['discount_factor'], quote['zero_rate'], quote['forward_rate'] = np.nan, np.nan, np.nan

    for tenor, date in zip(quote.index, quote['Maturity']):
        quote.loc[tenor, 'discount_factor'] = discount_factor(date, curve)
        quote.loc[tenor, 'zero_rate'] = zero_rate(date, curve) * 100
        quote.loc[tenor, 'forward_rate'] = forward_rate(date, curve) * 100

    print(quote[['discount_factor', 'zero_rate', 'forward_rate']])

    # plot the result
    plt.figure(figsize=(16,8))
    plt.plot(quote['zero_rate'], 'b-', label='zero curve')
    plt.plot(quote['forward_rate'], 'g-', label='forward curve')
    plt.title('zero and forward curve', loc='center')
    plt.legend()
    plt.xlabel('maturity')
    plt.ylabel('interst rate')


    # plot the result
    plt.figure(figsize=(16,8))
    plt.plot(quote['discount_factor'], 'r-', label='discount curve')
    plt.title('discount curve', loc='center')
    plt.legend()
    plt.xlabel('maturity')
    plt.ylabel('discount factor')