from tiingoAPI import *
import datetime


def getName(code):
    return getMeta(code)['name']


def getLastPrice(code):
    return getTopOfBookPrice(code)[0]['last']


def getPrevChange(code):
    data = getTopOfBookPrice(code)[0]
    prevPrice = data['prevClose']
    currPrice = data['last']

    return (currPrice - prevPrice)/prevPrice


def getLastPriceOfAll(codes):
    data = getTopOfBookOfAll(codes)
    ans = list()
    for d in data:
        ans.append(d['last'])

    return ans
