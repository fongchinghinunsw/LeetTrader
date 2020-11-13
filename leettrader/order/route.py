"""
  Routing of Stock Order Placing
"""

from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user

from leettrader.user.forms import (OrderForm, CheckoutForm)
from leettrader.order.utils import *
from leettrader.stock.utils import get_search_result
from leettrader.models import Stock


def order_stock(stock, action):
  ''' Routing of Order Form '''
  # If user submit the Order Form
  order_form = OrderForm()
  if order_form.validate_on_submit():

    # Read user inputs from Order Form
    qty = order_form.quantity.data
    t_type = order_form.transaction_type.data

    # Check if transaction amt > $1
    if not check_min_order(stock, int(qty)):
      flash('Transaction amount should be larger than $1.', "danger")
    
    # If the order is legal, direct to checkout page
    elif check_legal_order(stock, action, qty):
      return redirect(url_for('users.checkout', action=action,
                              stock=stock, quantity=qty, transaction_type=t_type))

    # Else, show flash message of error
    else:
      flash('You do not have enough amount of this stock to sell', "danger") 
  
  #Direct to Order Page
  return render_template('order.html', title='order',
                         stock=stock, action=action, order_form=order_form)


def checkout_stock(stock, action):
  ''' Routing for Checkout Form'''
  # Read Inputs from Checkout form & Database
  uid = current_user.get_id()
  qty = request.args.get('quantity')
  stock_obj = Stock.query.filter_by(code=stock).first()
  sid = stock_obj.id

  # Calculate total checkout price, display it on checkout page
  unit_price = get_search_result(stock_obj.code)['price']
  tot_price = float(unit_price) * int(qty)
  checkout_form = CheckoutForm(current_market_price=unit_price, total_price=str(tot_price))

  # When user submit the checkout form
  if checkout_form.validate_on_submit():
    # If user click cancel button, back to search page
    if checkout_form.cancel.data:
      return redirect(url_for('stocks.search_page', code=stock_obj.code))

    # Else, update database & return home
    new_qty = update_own_stock(uid, sid, action, int(qty), tot_price)
    flash_msg = get_order_success_msg(action, stock, new_qty)
    flash(flash_msg, "success")
    create_transaction_record(uid, action, stock_obj, qty, checkout_form)
    return redirect(url_for('users.home'))

  # Return Checkout Page    
  return render_template('checkout.html',
                         title='checkout',
                         stock_obj=stock_obj,
                         action=action,
                         quantity=qty,
                         checkout_form=checkout_form)
