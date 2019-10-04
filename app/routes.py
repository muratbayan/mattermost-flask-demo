from app import app
from flask import request
from flask import make_response
import requests
import json

def format_forex_data(source, target, refreshDate, value):
    
    hyperlink_value = """[%s](https://www.xe.com/currencycharts/?from=%s&to=%s&view=1D)""" % (value, source, target)

    formatted_data = """#### Forex Query Results \n| Source  | Target   | Last Refresh Date | Value |\n|:--------|:--------:|:------------------|:------|\n| %s      | %s       | %s                | %s    |""" % (source, target, refreshDate, hyperlink_value)

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

    if "text" in args:
        queryText = args["text"]

    if len(queryText) == 0:
        source = "GBP"
        target = "EUR"
    else:
        (source, target) = queryText.split()
    
    forex_data = get_forex_data(source.upper(), target.upper())

    if request.method == "POST":
        return "this is a POST request"

    resp = make_response(forex_data)
    resp.headers['Content-Type'] = 'application/json'

    return resp