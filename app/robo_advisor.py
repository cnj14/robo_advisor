# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

load_dotenv()

now = datetime.now()
current_time = now.strftime("%I:%M%p on %Y-%m-%d")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops")
count = 0
n = (input("How many stocks would you like to consider? "))
if n.isnumeric() == True:
    n = int(n)
    while count < n:
        SYMBOL = input("Please input a company ticker: ")
        chars = list(SYMBOL)
        if SYMBOL.isalpha()==True and len(chars)<=5:
            request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
            response = requests.get(request_url)
            if "Error Message" in response.text:
                print("Error received; please try again! Enter a valid ticker such as 'AAPL' or 'VZ'.")
            else:
                print("ACCESSING DATA...")
                parsed_response = json.loads(response.text)
                tsd = parsed_response["Time Series (Daily)"]
                mdata = parsed_response["Meta Data"]
                csv_file_path = f"data/{SYMBOL}.csv"
                with open(csv_file_path,"w") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open","high","low","close","volume"])
                    writer.writeheader()
                    for date,values in tsd.items():
                        writer.writerow({"timestamp": date, "open": values["1. open"], "high": values["2. high"], "low": values["3. low"], "close": values["4. close"], "volume": values["5. volume"]})
                print("------------------------------------")
                print(f"Stock selected: {SYMBOL}")
                print(f"Program run at {current_time}")
                latest = mdata["3. Last Refreshed"]
                print(f"Latest data from {latest}")
                print("------------------------------------")
                with open(csv_file_path, "r") as csv_file: 
                    reader = csv.DictReader(csv_file) 
                    all_closes = []
                    all_highs = []
                    all_lows = []
                    dates = []
                    for row in reader:
                        close = float(row["close"])
                        all_closes.append(close)
                        high = float(row["high"])
                        all_highs.append(high)
                        low = float(row["low"])
                        all_lows.append(low)
                        date = row["timestamp"]
                        dates.append(date)
                    last_close = (all_closes[0])
                    last_close = '${:,.2f}'.format(last_close)
                    recent_max = max(all_highs)
                    recent_max = '${:,.2f}'.format(recent_max)
                    recent_min = min(all_lows)
                    recent_min = '${:,.2f}'.format(recent_min)
                print(f"Most recent closing price: {last_close}")
                print(f"Recent high price: {recent_max}")
                print(f"Recent low price: {recent_min}")
                for p in all_closes:
                    p = "${0:.2f}".format(p)
                all_closes.reverse()
                fig1, ax = plt.subplots()
                ax.plot(dates, all_closes)
                formatter = ticker.FormatStrFormatter('$%1.2f')
                ax.yaxis.set_major_formatter(formatter)
                plt.title(f"{SYMBOL} Stock (Last 100 Days)")
                fig1.autofmt_xdate()
                every_nth = 9
                for n, label in enumerate(ax.xaxis.get_ticklabels()):
                    if n % every_nth != 0:
                        label.set_visible(False)
                plt.show()
                print("------------------------------------")
                print("------------------------------------")
                print("RUNNING PROPRIETARY INVESTMENT ALGORITHM...")
                print("------------------------------------")
                count+=1
        else:
            print("Please try an alphabetic ticker with 5 or fewer letters.")
    print("Thank you for using the Robo Advisor! Happy investing :)")
else:
    print("Invalid number of stocks entered. Please run code again!")
    exit()



