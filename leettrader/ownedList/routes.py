"""
  Routing of Owned List
"""

from flask import Blueprint, jsonify
from leettrader.stock.utils import get_search_result
from flask_login import current_user, login_required

from leettrader import db
from leettrader.stock.utils import get_search_result
from leettrader.models import Watchlist, Stock, OwnStock
from leettrader.formatter import format_owned_info, color_span


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
  tot_PL = 0
  
  # Access database, get list of owned stocks from user id
  ol = db.session.query(OwnStock).filter(
      OwnStock.user_id == current_user.get_id()).all()

  # For each owned stock, create a HTML formatted string
  for item in ol:
    # Get information of a owned stock
    stockInfo = getStockInfo(item.stock_id)
    name = stockInfo[0]
    market = stockInfo[1] * int(item.unit)
    currency = stockInfo[2]
    purchase = float(item.total_purchase_price)

    # Calculate P/L
    pl = round(market-purchase, 2)
    tot_PL += pl

    # Format Info & P/L into <div> and <span>
    ownedListItem = format_owned_info(name, item.unit, currency, market, purchase, pl)
    ans_list.append(ownedListItem)
    tot_PL_html = color_span(tot_PL)
  
  return [ans_list, tot_PL_html]


def getStockInfo(stockID):
  ''' Return stock information of a stock '''
  target = db.session.query(Stock).filter(
      Stock.id == int(stockID)).first()
  
  info = get_search_result(target.code)
  marketPrice = float(info['price'])
  currency = info['currency']
  
  return [target.name, marketPrice, currency]