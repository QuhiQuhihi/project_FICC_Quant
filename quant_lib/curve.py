import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests

from bs4 import BeautifulSoup
import QuantLib as ql

def get_date():
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get('https://www.wsj.com/market-data/bonds', headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find("span", class_ = "WSJBase--card__timestamp--3F2HxyAE")
    
    # JS path
    # document.querySelector("#root > div > div > div > div:nth-child(2) > div.style--grid--SxS2So51 > div > div:nth-child(2) > h3 > span.WSJBase--card__timestamp--3F2HxyAE > span")

    date = data.text
    date = datetime.datetime.strptime(date, "%m/%d/%y").date()
    return date

def get_quote(reference_date):
    tenors = ['01M', '03M', '06M', '01Y', '02Y', '03Y','05Y','07Y','10Y','30Y']

    # create empty lists
    maturities = []
    days = []
    prices = []
    coupons = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # get market informations
    for i, tenor in enumerate(tenors):
        url = "https://www.wsj.com/market-data/quotes/bond/BX/TMUBMUSD"+tenor+"?mod=md_bond_overview_quote"
        req = requests.get(url, headers=headers)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # Price 
        data_src = soup.find("span", id="quote_val") 
        price = data_src.text
        price = float(price[:-1])
    
        data_src2 = soup.find_all("span", class_="data_data")

        # Coupon
        coupon = data_src2[2].text
        if coupon != '':
            coupon = float(coupon[:-1])
        else:
            coupon = 0.0
        
        # Maturity Date
        maturity = data_src2[3].text
        maturity = datetime.datetime.strptime(maturity, '%m/%d/%y').date()

        # Send to lists
        days.append((maturity - reference_date).days)
        prices.append(price)
        coupons.append(coupon)
        maturities.append(maturity)
    
    # create dataframe
    df = pd.DataFrame([maturities, days, prices, coupons]).transpose()
    headers = ['maturity', 'days', 'price', 'coupon']
    df.columns = headers
    df.set_index('maturity', inplace=True)

    return df

def treasury_curve(date, quote):
    
    # Divide Quotes
    tbill = quote[0:4]
    tbond = quote[4:]
    
    # Set Evaluation Date
    eval_date = ql.Date(date.day, date.month, date.year)
    ql.Settings.instance().evaluationDate = eval_date
    
    # Set Market Conventions
    calendar = ql.UnitedStates()
    convention = ql.ModifiedFollowing
    day_counter = ql.ActualActual()
    end_of_month = False
    fixing_days = 1
    face_amount = 100
    coupon_frequency = ql.Period(ql.Semiannual)
    
    # Construct Treasury Bill Helpers
    bill_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)),
                                         ql.Period(m, ql.Days),
                                         fixing_days,
                                         calendar,
                                         convention,
                                         end_of_month,
                                         day_counter)
                    for r, m in zip(tbill['price'], tbill['days'])]
    
    # Construct Treasury Bond Helpers
    bond_helpers = []
    for p, c, m in zip(tbond['price'], tbond['coupon'], tbond['days']):
        termination_date = eval_date + ql.Period(m, ql.Days)
        schedule = ql.Schedule(eval_date,
                               termination_date,
                               coupon_frequency,
                               calendar,
                               convention,
                               convention,
                               ql.DateGeneration.Backward,
                               end_of_month)
        bond_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(100)),
                                             fixing_days,
                                             face_amount,
                                             schedule,
                                             [c/100.0],
                                             day_counter,
                                             convention)
        bond_helpers.append(bond_helper)
    
    # Bind Helpers
    rate_helper = bill_helpers + bond_helpers
    
    # Build Curve
    yc_linearzero = ql.PiecewiseLinearZero(eval_date, rate_helper, day_counter)
    
    return yc_linearzero

def discount_factor(date, curve):
    # returns discount factors of each day
    # use quantlib date type
    print(date)
    date = ql.Date(date.day, date.month, date.year)
    return curve.discount(date)

def zero_rate(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    day_counter = ql.ActualActual()
    compounding = ql.Compounded
    freq = ql.Continuous
    zero_rate = curve.zeroRate(date, day_counter, compounding, freq).rate()
    return zero_rate
