# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

load_dotenv()

now = datetime.now()
current_time = now.strftime("%I:%M%p on %Y-%m-%d")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops")
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
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
        response = requests.get(request_url)
        if "Error Message" in response.text:
            print("Error received; please try again! Enter a valid ticker such as 'AAPL' or 'VZ'.")
        else:
            print("------------------------------------")
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
                last_close_1 = '${:,.2f}'.format(last_close)
                recent_max = max(all_highs)
                recent_max_1 = '${:,.2f}'.format(recent_max)
                recent_min = min(all_lows)
                recent_min_1 = '${:,.2f}'.format(recent_min)
            print(f"Most recent closing price: {last_close_1}")
            print(f"Recent high price: {recent_max_1}")
            print(f"Recent low price: {recent_min_1}")
            for p in all_closes:
                p = "${0:.2f}".format(p)
            all_closes.reverse()
            dates.reverse()
            fig1, ax = plt.subplots()
            ax.plot(dates, all_closes)
            formatter = ticker.FormatStrFormatter('$%1.2f')
            ax.yaxis.set_major_formatter(formatter)
            plt.title(f"{SYMBOL} Stock (Last 100 Days)")
            fig1.autofmt_xdate()
            # https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks/13418954#13418954
            every_nth = 9
            for n, label in enumerate(ax.xaxis.get_ticklabels()):
                if n % every_nth != 0:
                    label.set_visible(False)
            plt.show()
            print("------------------------------------")
            print("RUNNING PROPRIETARY INVESTMENT ALGORITHM...")
            daily_returns = []
            gains = []
            losses = []
            all_closes.reverse()
            for i in range(99):
                r = all_closes[i]-all_closes[i+1]
                r = r/all_closes[i+1]
                daily_returns.append(r)
            for r in daily_returns:
                if r>0:
                    gains.append(r)
                else:
                    losses.append(r)
            price_range = (recent_max-recent_min)
            midpoint = (recent_min + recent_max)/2
            percentile = 100*((last_close-recent_min)/price_range)
            percentile = '{:,.2f}'.format(percentile)
            print(f"In the last 100 days, {SYMBOL} has had {len(gains)} daily gains \nand {len(losses)} daily losses from close to close.")
            print('')
            print(f"{SYMBOL} is currently priced at {last_close_1} which is \n in the {percentile} percentile of the 100-day range.")
            print('')
            if len(gains)>55 and midpoint>last_close:
                print(f"{SYMBOL} has had daily gains more than 55% of the time and is \n still closer to its recent low than high.")
                print(f"We recommend {SYMBOL} as a BUY opportunity.")
            elif len(gains)>55 and midpoint<last_close:
                print(f"{SYMBOL} has had daily gains more than 55% of the time but is \n closer to its recent high than low.")
                print(f"We recommend HOLDING for the moment on {SYMBOL}.")
            elif len(gains)<55 and midpoint>last_close:
                print(f"{SYMBOL} is closer to its recent low than high, but \n has had daily gains less than 55% of the time.")
                print(f"We recommend HOLDING for the moment on {SYMBOL} but watching closely.")
            elif len(gains)<55 and midpoint<last_close:
                print(f"{SYMBOL} is closer to its recent high than low and \n has had daily gains less than 55% of the time.")
                print(f"We recommend {SYMBOL} as a SELL opportunity.")
            print("------------------------------------")
    print("Thank you for using the Robo Advisor! Happy investing :)")
else:
    print("Invalid number of stocks entered. Please run code again!")
    exit()



