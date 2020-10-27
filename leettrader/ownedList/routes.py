"""
  Routing of Owned List
"""

from flask import Blueprint, jsonify
from leettrader.stock.utils import get_search_result
from flask_login import current_user, login_required

from leettrader import db
from leettrader.stock.utils import get_search_result
from leettrader.models import Watchlist, Stock, OwnStock


ownedList = Blueprint('ownedList', __name__)


@ownedList.route('/get_ownedList', methods=['GET'])
@login_required
def get_ownedList():
  ''' Return list of owned stocks in JSON format '''
  ans = get_ownedlist_from_db()
  return jsonify(ownedList=ans), 200




def get_ownedlist_from_db():
  ''' Return list of owned stocks '''
  ans_list = []
  
  # Access database, get list of owned stocks from user id
  ol = db.session.query(OwnStock).filter(
      OwnStock.user_id == current_user.get_id()).all()

  # For each owned stock, create a list: 
  # [StockName, Qty, tot_PurchasePrice, tot_MarketPrice, P/L, color]
  for item in ol:
    # Get information of stock - [Name, MarketPrice]
    stockInfo = getStockInfo(item.stock_id)

    # Compute information of list
    name = stockInfo[0]
    market = stockInfo[1] * int(item.unit)
    purchase = float(item.total_purchase_price)
    tot_PL = market - purchase
    color = colorOfPL(tot_PL)

    # Round all numbers to 2 d.p
    market = round(market, 2)
    purchase = round(purchase, 2)
    tot_PL = round(tot_PL, 2)
    
    # Append list to ans_list
    ans_list.append([name, item.unit, market, purchase, tot_PL, color])
  
  return ans_list


def getStockInfo(stockID):
  ''' Return stock information of a stock '''
  target = db.session.query(Stock).filter(
      Stock.id == int(stockID)).first()
  
  info = get_search_result(target.code)
  marketPrice = float(info['price'])
  
  return [target.name, marketPrice]


def colorOfPL(PL):
  ''' Return colour of P/L '''
  if PL >= 0:
    return "green"
  
  return "red"