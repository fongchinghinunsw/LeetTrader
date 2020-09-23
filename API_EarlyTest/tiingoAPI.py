
import json
import requests

# Date format = "2019-01-02"
api_Tiingo = "https://api.tiingo.com/tiingo/"
token_Tiingo = "b877591298ac6554d6a168729f67be31c604742b"
headers = {'Content-Type': 'application/json'}


def getMeta(code):
    url = api_Tiingo + "daily/" + code + "?token=" + token_Tiingo
    return requests.get(url, headers=headers).json()


def getEndOfDayPrice(code):
    url = api_Tiingo + "daily/" + code + "/prices?" + "&token=" + token_Tiingo
    return (requests.get(url, headers=headers).json())


def getHistPrices(code, start):
    url = api_Tiingo + "daily/" + code
    url += "/prices?startDate=" + start
    url += "&token=" + token_Tiingo

    return (requests.get(url, headers=headers).json())


# This methods can be used to return a list of companies data
def getTopOfBookPrice(code):
    url = "https://api.tiingo.com/iex/?tickers=" + code + "&token=" + token_Tiingo
    r = requests.get(url, headers=headers)
    return r.json()


def getTopOfBookOfAll(codes):
    codeStr = ""
    for c in codes:
        codeStr += c + ","

    codeStr = codeStr[:-1]

    return getTopOfBookPrice(codeStr)
