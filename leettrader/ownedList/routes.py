"""
  Routing of Owned List
"""

from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from leettrader import db
from leettrader.models import Stock, OwnStock
from leettrader.formatter import owned_table_item, color_span_2dp
from leettrader.stock.utils import get_search_result


ownedList = Blueprint('ownedList', __name__)


@ownedList.route('/get_ownedList', methods=['GET'])
@login_required
def get_owned_list():
  ''' Initialize Banks, Return Balance Sheet '''
  # If user doesn't have bank a/c yet, create a/c
  if current_user.balance == {}:
    print("Initialize bank accounts ... ")
    current_user.balance = {'AUD': 0.00, 'NZD': 0.00}
    db.session.commit()
  
  print("Balance already initialized. Now print balance sheet.")
  print(current_user.balance)

  ans = get_ownedlist_from_db()
  return jsonify(ownedList=ans), 200




def get_ownedlist_from_db():
  ''' Return list of owned stocks '''
  nz_list = []
  au_list = []
  nz_profit = 0
  au_profit = 0
  nz_worth = 0
  au_worth = 0
  nz_bank = current_user.balance['NZD']
  au_bank = current_user.balance['AUD']

  # Access database, get list of owned stocks from user id
  own_list = db.session.query(OwnStock).filter(
      OwnStock.user_id == current_user.get_id()).all()

  NZisColorGrey = False
  AUisColorGrey = False
  # For each owned stock, create a HTML formatted string
  for item in own_list:
    # Get information of a owned stock
    stock_info = get_stock_info(item.stock_id)
    name = stock_info[0]
    code = stock_info[1]
    market = stock_info[2] * int(item.unit)
    currency = stock_info[3]
    purchase = float(item.total_purchase_price)

    # Calculate Profit & Format Information as HTML Tags
    profit = round(market-purchase, 4)

    # NZ Stocks
    if currency == "NZD":
      item = owned_table_item(name, code, item.unit, currency, market, purchase, profit, NZisColorGrey)
      NZisColorGrey = True if False else True
      nz_profit += profit
      nz_worth += purchase
      nz_list.append(item)

    # AU Stocks
    elif currency == "AUD":
      item = owned_table_item(name, code, item.unit, currency, market, purchase, profit, AUisColorGrey)
      AUisColorGrey = True if False else True
      au_profit += profit
      au_worth += purchase
      au_list.append(item)

  # Calculate net worths of users, return balance sheet in HTML format
  nz_tot = nz_bank + nz_worth
  au_tot = au_bank + au_worth
  return [nz_list, color_span_2dp(nz_profit), au_list, color_span_2dp(au_profit),
          color_span_2dp(nz_worth), color_span_2dp(au_worth),
          color_span_2dp(nz_bank), color_span_2dp(au_bank),
          color_span_2dp(nz_tot), color_span_2dp(au_tot)]


def get_stock_info(stock_id):
  ''' Return stock information of a stock '''
  target = db.session.query(Stock).filter(
      Stock.id == int(stock_id)).first()

  info = get_search_result(target.code)
  worth = float(info['price'])
  currency = info['currency']

  return [target.name, target.code, worth, currency]
