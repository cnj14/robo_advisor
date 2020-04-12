# test/advisor_test.py

import os
import csv
import pytest
from app.robo_advisor import to_usd, get_response, transform_response, csv_writer, get_decision

CI_ENV = os.environ.get("CI") == "true" 
@pytest.mark.skipif(CI_ENV==True, reason="to avoid configuring credentials on, and issuing requests from, the CI server")

def test_to_usd():
    # function should add dollar sign and transform numeric object into string
    assert to_usd(4.50) == '$4.50'
    # function should round to two decimal places
    assert to_usd(4.5) == '$4.50'
    assert to_usd(4.5555) == '$4.56'
    # function should apply commas for numbers greater than 1,000
    assert to_usd(1234567890.5555) == '$1,234,567,890.56'

def test_get_response():
    sample = get_response("AAPL")
    # function should return a dict object
    assert type(sample) == dict
    # dict object keys should be as follows
    assert 'Meta Data' and 'Time Series (Daily)' in sample.keys()

def test_transform_response():
    # function should read through JSON data to output dictionary of Daily Time Series data parsed by timestamp
    parsed_response = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "MSFT",
            "3. Last Refreshed": "2018-06-08",
            "4. Output Size": "Full size",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2019-06-08": {
                "1. open": "101.0924",
                "2. high": "101.9500",
                "3. low": "100.5400",
                "4. close": "101.6300",
                "5. volume": "22165128"
            },
            "2019-06-07": {
                "1. open": "102.6500",
                "2. high": "102.6900",
                "3. low": "100.3800",
                "4. close": "100.8800",
                "5. volume": "28232197"
            }
        }
    }

    transformed_response = [
        {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128},
        {"timestamp": "2019-06-07", "open": 102.65, "high": 102.69, "low": 100.38, "close": 100.88, "volume": 28232197}
    ]

    assert transform_response(parsed_response) == transformed_response

def test_csv_writer():
    # function will test whether the csv.DictWriter has worked correctly
    # this tests the headers of the CSV file and the first value in the 'open' column
    sample = [
        {"timestamp": "2019-06-08", "open": 101.0924, "high": 101.95, "low": 100.54, "close": 101.63, "volume": 22165128}
    ]
    csv_writer('SAMPLE', sample)
    filepath = 'data/SAMPLE.csv'
    with open(filepath, 'r') as csv_filepath:
        reader = csv.DictReader(csv_filepath)
        for row in reader:
            assert 'timestamp' and 'open' and 'high' and 'low' and 'close' and 'volume' in row.keys()
            assert row['open'] == '101.0924'

def test_get_decision():
    # function will test math behind advisory decision 
    symbol = 'Sample'
    sample_close = 180
    sample_low = 100 
    sample_high = 200
    assert get_decision(symbol, sample_close, sample_high, sample_low) == 'SELL! SAMPLE IS PRICED CLOSER TO ITS RECENT HIGH THAN LOW.'


    


