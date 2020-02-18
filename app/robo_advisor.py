# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "oops")
SYMBOL = input("Please input a company ticker: ")
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=5min&apikey={API_KEY}"
print("URL:", request_url)

response = requests.get(request_url)
if "Error Message" in response.text:
    print("Error received")
    exit()
parsed_response = json.loads(response.text)



print(parsed_response)


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

