"""
  Routing of Owned List
"""

from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from leettrader import db
from leettrader.models import Stock, OwnStock
from leettrader.formatter import format_owned_info, color_span
from leettrader.stock.utils import get_search_result


ownedList = Blueprint('ownedList', __name__)


@ownedList.route('/get_ownedList', methods=['GET'])
@login_required
def get_owned_list():
  ''' Return list of owned stocks in JSON format '''
  ans = get_ownedlist_from_db()
  return jsonify(ownedList=ans), 200



def get_ownedlist_from_db():
  ''' Return list of owned stocks '''
  ans_list = []
  tot_pl = 0

  # Access database, get list of owned stocks from user id
  own_list = db.session.query(OwnStock).filter(
      OwnStock.user_id == current_user.get_id()).all()

  # For each owned stock, create a HTML formatted string
  for item in own_list:
    # Get information of a owned stock
    stock_info = get_stock_info(item.stock_id)
    name = stock_info[0]
    market = stock_info[1] * int(item.unit)
    currency = stock_info[2]
    purchase = float(item.total_purchase_price)

    # Calculate P/L
    profit = round(market-purchase, 2)
    tot_pl += profit

    # Format Info into <div>
    item = format_owned_info(name, item.unit, currency, market, purchase, profit)
    ans_list.append(item)

  return [ans_list, color_span(tot_pl)]


def get_stock_info(stock_id):
  ''' Return stock information of a stock '''
  target = db.session.query(Stock).filter(
      Stock.id == int(stock_id)).first()

  info = get_search_result(target.code)
  worth = float(info['price'])
  currency = info['currency']

  return [target.name, worth, currency]
