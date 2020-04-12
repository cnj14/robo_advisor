# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv() # loads .env file contents so we can retrieve API key using os below

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops") 

now = datetime.now()
current_time = now.strftime("%I:%M%p on %Y-%m-%d")

def lines():
    """
    Aesthetic function to simplify code for receipt output.
    """
    print("------------------------------------")

def to_usd(price):
    """
    Returns a numeric object in USD format.
    Example: to_usd(5) or to_usd(41.2)
    """
    return "${0:,.2f}".format(price)

def get_symbols():
    """
    Asks user to input stock tickers for advising.
    User can run as many inputs as desired by pre-selecting # of tickers.
    """
    count = 0
    if __name__ == "__main__":
        n = (input("How many stocks would you like to consider? "))
        if n.isnumeric() == True:
            n = int(n)
        else:
            print("Invalid number of stocks entered. Please run code again!")
            exit()
    if __name__ == "__main__":
        while count < n:
            SYMBOL = input("Please input a company ticker: ")
            chars = list(SYMBOL)
            if SYMBOL.isalpha()==True and len(chars)<=5:
                symbols.append(SYMBOL)
                count +=1
            else:
                print("Please try an alphabetic ticker with 5 or fewer letters.")
    return symbols

def get_response(symbol):
    """
    Sends web request to alpahavantage to get stock data using API key from .env file
    Returns parsed response as JSON object 
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    """
    Turns JSON object (from get_response function) into a dictionary with keys "Meta Data" and "Time Series Daily"
    """
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

def csv_writer(symbol, rows):
    """
    Writes to a new file for stock data, converting dictionary element into CSV format.
    Files stored locally in data folder but hidden from master repo using gitignore.
    """
    symbol = symbol.upper()
    filepath = f"data/{symbol}.csv"
    with open(filepath, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return True

def get_decision(symbol,last,high,low):
    """
    Decision algorithm for stock recommendations.
    Calculates midpoint between recent high and low prices. 
    If current price is less than midpoint, algorithm recommends a BUY.
    """
    diff = high - low
    midpoint = low + diff/2
    symbol = symbol.upper()
    if last<midpoint:
        return f'BUY! {symbol} IS PRICED CLOSER TO ITS RECENT LOW THAN HIGH.'
    else:
        return f'SELL! {symbol} IS PRICED CLOSER TO ITS RECENT HIGH THAN LOW.'

symbols = []
get_symbols()
for SYMBOL in symbols:
    parsed_response = get_response(SYMBOL)
    latest = parsed_response["Meta Data"]["3. Last Refreshed"]
    rows = transform_response(parsed_response)
    csv_writer(SYMBOL,rows)
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



