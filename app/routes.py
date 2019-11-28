from app import app
from flask import request
from flask import make_response
import requests
import json
import random

def format_forex_data(source, target, refreshDate, value):
    
    hyperlink_value = """[%s](https://www.xe.com/currencycharts/?from=%s&to=%s&view=1D)""" % (value, source, target)

    formatted_data = """#### Forex Query Results \n| Source  | Target   | Last Refresh Date | Value |\n|:--------|:--------:|:------------------|:------|\n| %s      | %s       | %s                | %s    |""" % (source, target, refreshDate, hyperlink_value)

    return formatted_data

def format_stock_data(stockname, price, previous_close, change_pct):
    
    hyperlink_value = """[%s](https://finance.yahoo.com/quote/%s/)""" % (price, stockname)

    change_value = float(change_pct.strip('%'))/100

    if change_value < -0.05:
        change_symbol = ":arrow_double_down: "
    elif change_value < 0:
        change_symbol = ":arrow_down_small: "
    elif change_value > 0.05:
        change_symbol = ":arrow_double_up: "
    elif change_value > 0:
        change_symbol = ":arrow_up_small: "
    else:
        change_symbol = ""



    formatted_data = """#### Stock Query Results \n| Symbol  | Price   | Previous Close | PCT Change |\n|:--------|:--------:|:------------------|:------|\n| %s      | %s       | %s                | %s    |""" % (stockname, hyperlink_value, previous_close, change_symbol + change_pct)

    return formatted_data

def format_holiday_data(holidaycount):

    formatted_data = """#### Holiday Allowance Overview \n| Allowance | Used   | Remaining |\n|:----------|:------:|:-----------|\n| 25      | %s       | %s                |""" % (holidaycount, 25 - holidaycount)

    return formatted_data

def get_forex_data(source, target):
    r = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=%s&to_currency=%s&apikey=F657FR56IL7YYX7G" % (source, target))

    json_result = json.loads(r.text)
    exchange_rate = json_result.get("Realtime Currency Exchange Rate").get("5. Exchange Rate")
    refresh_date = json_result.get("Realtime Currency Exchange Rate").get("6. Last Refreshed")

    formatted_data = format_forex_data(source, target, refresh_date, exchange_rate)

    response_dict = {
        'text': formatted_data,
        'username' : "Forex Service",
        'icon_url' : "https://cdn2.iconfinder.com/data/icons/accounting-auditors-1/66/80-512.png"
        }

    response_json = json.dumps(response_dict)
    
    return response_json

def get_stock_data(stockname):
    r = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=F657FR56IL7YYX7G" % stockname)

    json_result = json.loads(r.text)
    price = json_result.get("Global Quote").get("05. price")
    previous_close = json_result.get("Global Quote").get("08. previous close")
    change_pct = json_result.get("Global Quote").get("10. change percent")

    formatted_data = format_stock_data(stockname, price, previous_close, change_pct)

    response_dict = {
        'text': formatted_data,
        'username' : "Stock Service",
        'icon_url' : "https://cdn0.iconfinder.com/data/icons/computing-3/66/candles_diagram_stock_price_climb_2-256.png"
        }

    response_json = json.dumps(response_dict)
    
    return response_json

def get_holiday_data(holiday_count):
    formatted_data = format_holiday_data(holiday_count)

    response_dict = {
        'text': formatted_data,
        'username' : "Holiday Service"
        }

    response_json = json.dumps(response_dict)
    
    return response_json

def get_forex_data2(source, target):
    r = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=%s&to_currency=%s&apikey=F657FR56IL7YYX7G" % (source, target))

    json_result = json.loads(r.text)
    exchange_rate = json_result.get("Realtime Currency Exchange Rate").get("5. Exchange Rate")
    refresh_date = json_result.get("Realtime Currency Exchange Rate").get("6. Last Refreshed")

    formatted_data = format_forex_data(source, target, refresh_date, exchange_rate)

    formatted_response_content = """{"text": "%s"}""" % formatted_data
    return formatted_response_content

#def create_mattermost_response(inputData):
#    resp = make_response()

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Mattermost!"
@app.route('/forex', methods=["GET","POST"])
def forex():

    args = request.args
    queryText = ""

    if request.method == "POST":
        content_text = request.get_json()['text']
        (_, source, target) = content_text.split()

    else:

        if "text" in args:
            queryText = args["text"]

        if len(queryText) == 0:
            source = "GBP"
            target = "EUR"
        else:
            (source, target) = queryText.split()
    
    forex_data = get_forex_data(source.upper(), target.upper())

    resp = make_response(forex_data)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/stock', methods=["GET","POST"])
def stocks():

    args = request.args
    queryText = ""
    if request.method == "POST":
        content_text = request.get_json()['text']
        (_, stock) = content_text.split()

    else:

        if "text" in args:
            queryText = args["text"]

        if len(queryText) == 0:
            stock = "MSFT"
        else:
            stock = queryText
        
    stock_data = get_stock_data(stock.upper())

    if request.method == "POST":
        print("POST data")
        print(stock_data)

    resp = make_response(stock_data)
    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route('/holiday', methods=["GET"])
def holiday():

    holiday_count = random.randrange(25)

    holiday_data = get_holiday_data(holiday_count)

    resp = make_response(holiday_data)
    resp.headers['Content-Type'] = 'application/json'

    return resp