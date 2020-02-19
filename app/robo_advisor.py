# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

now = datetime.now()
current_time = now.strftime("%I:%M%p on %Y-%m-%d")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops")
count = 0
n = int(input("How many stocks would you like to consider? "))
while count < n:
    SYMBOL = input("Please input a company ticker: ")
    chars = list(SYMBOL)
    if SYMBOL.isalpha()==True and len(chars)<=5:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"
        print("URL:", request_url)
        response = requests.get(request_url)
        if "Error Message" in response.text:
            print("Error received; please try again! Enter a valid ticker such as 'AAPL' or 'VZ'.")
        else:
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
            count+=1
    else:
        print("Please try a an alphabetic ticker with 5 or fewer letters.")



#print(parsed_response)

# tsd = parsed_response["Time Series (Daily)"]
# print(tsd)


# print("-------------------------")
# print("SELECTED SYMBOL: XYZ")
# print("-------------------------")
# print("REQUESTING STOCK MARKET DATA...")
# print("REQUEST AT: 2018-02-20 02:00pm")
# print("-------------------------")
# print("LATEST DAY: 2018-02-20")
# print("LATEST CLOSE: $100,000.00")
# print("RECENT HIGH: $101,000.00")
# print("RECENT LOW: $99,000.00")
# print("-------------------------")
# print("RECOMMENDATION: BUY!")
# print("RECOMMENDATION REASON: TODO")
# print("-------------------------")
# print("HAPPY INVESTING!")
# print("-------------------------")

