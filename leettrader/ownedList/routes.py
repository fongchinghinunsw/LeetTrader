"""
  Routing of Balance Sheet Displayed At Home
"""

from flask import Blueprint, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from leettrader import db
from leettrader.models import Stock, OwnStock
from leettrader.stock.utils import get_search_result
from leettrader.ownedList.bal_sheet import BalanceSheet
from leettrader.ownedList.reset import reset_account

ownedList = Blueprint('ownedList', __name__)


@ownedList.route('/get_ownedList', methods=['GET'])
@login_required
def get_owned_list():
  ''' Initialize Banks, Return Balance Sheet '''
  # If user doesn't have bank a/c yet, create bank a/c
  if current_user.balance == {}:
    current_user.balance = {'AUD': 0.00, 'NZD': 0.00}
    db.session.commit()

  # Get balance sheet, jsonify it & return
  ans = get_balance_sheet()
  return jsonify(ownedList=ans), 200

@ownedList.route('/accountResetting', methods=['GET'])
@login_required
def reset_user_account():
  reset_account()
  flash("Your account has been reset successfully !", "success")
  return redirect(url_for("users.home"))


def get_balance_sheet():
  ''' Return list of owned stocks '''
  # Initialize balance sheet object
  bal_sheet = BalanceSheet()

  # Access database, get user's owned stock list
  uid = current_user.get_id()
  own_list = db.session.query(OwnStock).filter(OwnStock.user_id == uid).all()

  # For each owned stock, update user's balance sheet
  for item in own_list:
    qty = item.unit
    purchase = float(item.total_purchase_price)
    stock_info = get_stock_info(item.stock_id)
    bal_sheet.update(stock_info, purchase, qty)

  return bal_sheet.get_final_bs()


def get_stock_info(sid):
  ''' Return information of a owned stock '''
  target = db.session.query(Stock).filter(Stock.id == int(sid)).first()

  info = get_search_result(target.code)
  worth = float(info['price'])
  currency = info['currency']
  return [target.name, target.code, worth, currency]
