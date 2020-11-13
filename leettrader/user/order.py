import operator
from datetime import datetime
from flask import render_template, url_for, flash, redirect, Blueprint, jsonify, request

from leettrader.user.forms import (OrderForm, CheckoutForm)
from leettrader.stock.utils import get_search_result
from leettrader.models import User, Stock, OwnStock, TransactionRecord
from leettrader import db
from flask_login import current_user
from leettrader.flash import get_order_success_msg


def check_legal_order(stock, action):
  ''' Interface to check if the order action is legal '''
  
  # When user submit the Order form, check if the action is legal
  order_form = OrderForm()
  if order_form.validate_on_submit():

    # Get input from Order form & Database
    qty = order_form.quantity.data
    transaction_type = order_form.transaction_type.data
    stock_id = Stock.query.filter_by(code=stock).first().id
    ownStock = OwnStock.query.filter_by(user_id=current_user.get_id(),
                                        stock_id=stock_id).first()

    # If the user is buying / having enough stock to sell, checkout successfully
    if action == "buy" or (ownStock is not None and ownStock.unit >= qty):
      print("You are " + action + "ing a stock.")
      return redirect(url_for('users.checkout',
                              action=action,
                              stock=stock,
                              quantity=qty,
                              transaction_type=transaction_type))

    # Otherwise, display error message
    flash('You do not have enough amount of this stock to sell', "danger")          
  
  # Render Order Form to UI
  return render_template('order.html', title='order',
                         stock=stock, action=action, order_form=order_form)


def checkout_stock(stock, action):
  ''' Checkout Order of a Stock '''
  # Read Inputs from Checkout form & Database
  uid = current_user.get_id()
  qty = request.args.get('quantity')
  transaction_type = request.args.get('transaction_type')
  stock_obj = Stock.query.filter_by(code=stock).first()
  stock_id = stock_obj.id
  current_market_price = get_search_result(stock_obj.code)['price']

  # Calculate total checkout price, display it on checkout page
  checkout_form = CheckoutForm(
    current_market_price=current_market_price,
    total_price=str(float(current_market_price) * int(qty))
  )

  # Action defined when user submit order form
  if checkout_form.validate_on_submit():
    return submit_checkout(uid, qty, stock_obj, stock_id, current_market_price, checkout_form, action, stock)

  print(checkout_form.data)
  return render_template('checkout.html',
                         title='checkout',
                         stock_obj=stock_obj,
                         action=action,
                         quantity=qty,
                         checkout_form=checkout_form)



def submit_checkout(uid, qty, stock_obj, stock_id, current_market_price, checkout_form, action, stock):
  # Return to Search Page if Cancel Order
  if checkout_form.cancel.data:
    return redirect(url_for('stocks.search_page', code=stock_obj.code))

  # Update user's owned stocks in Database
  ownStock = OwnStock.query.filter_by(user_id=uid, stock_id=stock_id).first()
  unit_change = int(qty)
  price_change = unit_change * float(current_market_price)
  update_own_stock(ownStock, stock_id, unit_change, price_change, action)

  # Display Flash Message
  if ownStock == None:
    flash_msg = get_order_success_msg(action, stock, unit_change)
  else:
    flash_msg = get_order_success_msg(action, stock, ownStock.unit)

  flash(flash_msg, "success")

  # Create Transaction Record, return
  create_transaction_record(uid, action, stock_obj, stock_id, qty, checkout_form)    
  return redirect(url_for('users.home'))



def update_own_stock(ownStock, sid, unit_change, price_change, action):
  # Calculate change of price and unit
  if action == "sell":
      unit_change *= -1
      price_change *= -1

  # Buy Stock at first time
  if ownStock is None:
      ownStock = OwnStock(user_id=current_user.get_id(), stock_id=sid,
                          unit=unit_change, total_purchase_price=price_change)
      db.session.add(ownStock)

  # Buy Stock / Sell Stock
  else:
    ownStock.unit += unit_change
    ownStock.total_purchase_price += price_change
    if ownStock.unit == 0:
      db.session.delete(ownStock) # Delete Tuple if Ownstock is Zero

  db.session.commit()


def create_transaction_record(uid, action, stock, sid, qty, checkout_form):
  action = {"buy": "BUY", "sell": "SELL"}[action]
  print(stock, "-----------------")
  record = TransactionRecord(user_id=current_user.get_id(), 
                              time=datetime.now(), action=action, 
                              stock=stock, stock_id=sid, 
                              quantity=qty, unit_price=checkout_form.data['current_market_price'])
  db.session.add(record)
  db.session.commit()
