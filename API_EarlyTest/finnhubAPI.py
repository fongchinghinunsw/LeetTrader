import json
import requests

# Stock code -> Stock name
# Stock code -> Latest avaiable unit price
# Percentage change in stock when comparing latest to prev day

api_Finnhub = "https://finnhub.io/api/v1/"
token_Finnhub = "bth7d9f48v6v983bgc70"


def getWebhook(event, company):
    url = api_Finnhub + "webhook/add?token="
    reqStr = url + token_Finnhub
    return requests.post(reqStr, json={'event': event, 'symbol': company})


def getProfile(code):
    url = api_Finnhub + "stock/profile2?symbol=" + code + "&token="
    reqStr = url + token_Finnhub
    return requests.get(reqStr)


def quote(code):
    url = api_Finnhub + "quotes?symbol=" + code
    reqStr = url + "&token=" + token_Finnhub
    return (requests.get(reqStr))


r = quote("AAPL")
print(r)
