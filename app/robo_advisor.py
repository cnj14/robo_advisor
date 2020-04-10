# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops")

now = datetime.now()
current_time = now.strftime("%I:%M%p on %Y-%m-%d")

def lines():
    print("------------------------------------")

def to_usd(price):
    return "${0:,.2f}".format(price)

def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, prices in tsd.items():
        row = {
            "timestamp": date,
            "open": float(prices["1. open"]),
            "high": float(prices["2. high"]),
            "low": float(prices["3. low"]),
            "close": float(prices["4. close"]),
            "volume": int(prices["5. volume"])
        }
        rows.append(row)
    return rows

def csv_writer(rows, filepath):
    with open(filepath, 'w') as csv_file:
        writer = csv_DictWriter(csv_file, fieldnames = ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return True

def get_decision(symbol,last,high,low):
    diff = high - low
    midpoint = low + diff/2
    symbol = symbol.upper()
    if last<midpoint:
        return f'BUY! {symbol} IS PRICED CLOSER TO ITS RECENT LOW THAN HIGH.'
    else:
        return f'SELL! {symbol} IS PRICED CLOSER TO ITS RECENT HIGH THAN LOW.'

count = 0
n = (input("How many stocks would you like to consider? "))
if n.isnumeric() == True:
    n = int(n)
    symbols = []
    while count < n:
        SYMBOL = input("Please input a company ticker: ")
        chars = list(SYMBOL)
        if SYMBOL.isalpha()==True and len(chars)<=5:
            symbols.append(SYMBOL)
            count +=1
        else:
            print("Please try an alphabetic ticker with 5 or fewer letters.")
    for SYMBOL in symbols:
        parsed_response = get_response(SYMBOL)
        latest = parsed_response["Meta Data"]["3. Last Refreshed"]
        
        rows = transform_response(parsed_response)
        last_close = rows[0]['close']
        high_prices = [row["high"] for row in rows]
        low_prices = [row["low"] for row in rows]
        recent_high = max(high_prices)
        recent_low = min(low_prices)

        lines()
        print(f"SYMBOL: {SYMBOL.upper()}")
        lines()
        print(f'REQUEST FULFILLED AT {current_time}')
        print(f'ACCESSING DATA FROM {latest}')
        lines()
        print(f"LATEST CLOSE: {to_usd(last_close)}")
        print(f"RECENT HIGH:  {to_usd(recent_high)}")
        print(f"RECENT LOW:   {to_usd(recent_low)}")
        lines()
        print('RUNNING PROPRIETARY INVESTMENT ALGORITHM...')
        print(f'RECOMMENDATION: {get_decision(SYMBOL,last_close,recent_high,recent_low)}')
        lines()
    print("Thank you for using the Robo Advisor! Happy investing :)")
else:
    print("Invalid number of stocks entered. Please run code again!")
    exit()


