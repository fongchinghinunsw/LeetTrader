'''
  Thie File provides support to functions related to Stock Trading of user, including:
  1. Check if the transaction is legal
  2. Update database if transcation is successful
'''

from datetime import datetime
from leettrader.stock.utils import get_search_result
from leettrader import db
from leettrader.models import Stock, OwnStock, TransactionRecord
from flask_login import current_user


def check_min_order(stock, qty):
  ''' Return True if transaction amt > 1.00 '''
  unit_price = get_search_result(stock)['price']
  tot_price = float(unit_price) * qty

  if tot_price < 1.0000:
    return False
  return True


def check_legal_order(stock, action, qty):
  ''' Return true if order is legal, false otherwise '''
  # Buy action must be legal
  if action == "buy":
    return True

  # Return False if user doesn't have this stock to sell
  sid = Stock.query.filter_by(code=stock).first().id
  own_stock = OwnStock.query.filter_by(user_id=current_user.get_id(),
                                       stock_id=sid).first()
  if own_stock is None:
    return False

  # Return False if user doesn't have enough stock to sell
  if own_stock.unit < qty:
    return False

  # The sell action is legal
  return True


def update_own_stock(uid, sid, action, qty, tot_price):
  ''' Update own stock of user, return the new owned qty of stock '''
  # Buy Stock at first time
  own_stock = OwnStock.query.filter_by(user_id=uid, stock_id=sid).first()
  if own_stock is None:
    own_stock = OwnStock(user_id=current_user.get_id(),
                         stock_id=sid,
                         unit=qty,
                         total_purchase_price=tot_price)
    db.session.add(own_stock)
    db.session.commit()
    return qty

  # Calculate change of total paid and qty, update database
  if action == "sell":
    qty *= -1
    tot_price *= -1
  own_stock.unit += qty
  own_stock.total_purchase_price += tot_price

  # Update bank balances of user
  update_bank(tot_price, sid)

  # Delete Tuple if own stock becomes zero after order
  if own_stock.unit == 0:
    db.session.delete(own_stock)

  db.session.commit()
  return own_stock.unit


def update_bank(price, sid):
  ''' Update bank balance after placing stock order '''
  target = db.session.query(Stock).filter(Stock.id == int(sid)).first()
  info = get_search_result(target.code)
  current_user.balance[info['currency']] -= price
  db.session.commit()


def create_transaction_record(uid, action, stock, qty, checkout_form):
  ''' Create transaction record in Database '''
  action = {"buy": "BUY", "sell": "SELL"}[action]
  record = TransactionRecord(
      user_id=uid,
      time=datetime.now(),
      action=action,
      stock=stock,
      stock_id=stock.id,
      quantity=qty,
      unit_price=checkout_form.data['current_market_price'])
  db.session.add(record)
  db.session.commit()


def get_order_success_msg(action, stock, unit):
  ''' Flash message after buy / sell stocks '''
  if action == "buy":
    flash_msg = "Brought " + stock + ". "
  else:
    flash_msg = "Sold " + stock + ". "

  return flash_msg + "You have " + str(unit) + " units of this stock remain."
