# robo_advisor


PATH:
/Users/christopherjayson/Desktop/robo_advisor

API setup:
https://www.alphavantage.co/support/#api-key

Obtain an API key at the website above

Create a new file in this repo called '.env'

Place the following contents in your .env file with your own API key in the blank:
ALPHAVANTAGE_API_KEY = "____________"

conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

pip install -r requirements.txt

python app/robo_advisor.py
