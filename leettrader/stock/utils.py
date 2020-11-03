"""
    Backend Support function for Search Page
"""

from random import choice
from datetime import datetime 
import requests
from bs4 import BeautifulSoup
from leettrader.models import Stock
from urllib import request
import csv 
import os

headers_list = [
    # Firefox 77 Mac
    {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]


def get_currency_by_stock_code(stock_code):
  market = Stock.query.filter_by(code=stock_code).first().market_type
  return {'NZ': 'NZD', 'AX': 'AUD'}[market.name]


def get_search_result(stock_code):
  ''' Get stock information from Stock Code '''

  source = requests.get(f'https://finance.yahoo.com/quote/{stock_code}',
                        headers=choice(headers_list)).text
  soup = BeautifulSoup(source, 'lxml')

  price = soup.find('span',
                    class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)").text
  change = soup.find('span',
                     class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)")

  if change is None:
    change = soup.find(
        'span',
        class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)")
  if change is None:
    change = soup.find(
        'span',
        class_="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)")

  change = change.text
  change = change.split()
  price_change = change[0]
  percent_change = change[1].strip("()")

  return {
      'currency': get_currency_by_stock_code(stock_code),
      'price': price,
      'price_change': price_change,
      'percent_change': percent_change
  }

def get_historical_data(stock_code):
    # eg stock_code = ANZ.AX
    curr_time = datetime.today()
    curr_time = int(curr_time.timestamp())
    prev_year = curr_time - 31622400
    request_url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true".format(stock_code, prev_year, curr_time)
    response = request.urlopen(request_url)
    csv = response.read()
    csv = str(csv).strip("b'")
    lines = csv.split("\\n")
    if not os.path.isdir("leettrader/stock/tmp/"):
        os.mkdir("leettrader/stock/tmp/")
    f = open("leettrader/stock/tmp/" + stock_code + ".csv", 'w')
    for line in lines:
        f.write(line +"\n")
    f.close()