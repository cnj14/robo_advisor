# robo_advisor

[![Build Status](https://travis-ci.com/cnj14/robo_advisor.svg?branch=master)](https://travis-ci.com/cnj14/robo_advisor)

1. Clone this repo to your computer and access via GitHub desktop

2. Obtain an API key at the website below:

https://www.alphavantage.co/support/#api-key

3. Open the repo in your external editor and create a new file in this repo called '.env'

4. Place the following contents in your .env file with your own API key in the blank:

ALPHAVANTAGE_API_KEY = "____________"

5. From Github Desktop, open this repo in your command line 

6. Run the following commands, one at a time, to setup the env and run/test the program!: 
```py
 conda create -n stocks-env python=3.7 # (first time only) 
 ```
```py
 conda activate stocks-env 
 ```
```py
 pip install -r requirements.txt 
 ```
```py
 pip install pytest
 ```
```py
 python app/robo_advisor.py
 ```
```py
 pytest
 ```