"""
  Routing of Search Page
"""
import os, re, os.path
from flask import render_template, request, redirect, url_for, Blueprint, flash, send_file
from flask_login import current_user, login_required
from leettrader.models import Stock, Watchlist
from leettrader.stock.forms import SearchStockForm
from leettrader.stock.utils import get_search_result, get_historical_data


stock = Blueprint('stocks', __name__)


@stock.route('/search', methods=['GET', 'POST'])
@login_required
def search_stock():
  ''' Check stock code, direct to Search Page '''
  # Get stock code
  stock_input = SearchStockForm(request.form).stock.data
  code = stock_input.split()[-1].strip("()")

  # Go to search page if stock code is valid, home page otherwise
  if Stock.query.filter_by(code=code).first():
    return redirect(url_for('stocks.search_page', code=code))

  flash("Please enter a valid stock name/code", "warning")
  return render_template('home.html')


@stock.route('/search/<string:code>')
@login_required
def search_page(code):
  ''' Route to Search Page '''
  stock_obj = Stock.query.filter_by(code=code).first()
  print(stock_obj.code)
  code = stock_obj.code
  result = get_search_result(code)
  stock = f"{ stock_obj.name } ({ stock_obj.code })"
  currency = result['currency']

  if float(result['price_change']) == 0:
    color = "black"
  elif float(result['price_change']) > 0:
    color = "green"
  else:
    color = "red"
  print(result)

  # Check if stock is already in watchlist
  in_watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first()
  if in_watchlist is None:
    date_added = 0
    listed = False
  else:
    date_added = in_watchlist.date_added
    listed = True

  # Export "search_result.html" from template, passing in:
  # 1. Stock code & name
  # 2. Stock price, price changes
  # 3. Colour of label of price information
  # 4. Whether stock is already in stocklist
  return render_template('search_result.html',
                         currency=currency,
                         code=code,
                         stock=stock,
                         price=result['price'],
                         price_change=result['price_change'],
                         percent_change=result['percent_change'],
                         color=color,
                         listed=listed,
                         date=date_added)

@stock.route('/get_csv/<string:code>', methods=['GET'])
@login_required
def get_csv(code):
  tmp_bin = "leettrader/stock/tmp/"
  '''
  caching the csv file if called repeatedly, use for testing
  '''
  # if os.path.isfile("leettrader/stock/tmp/"+ code + ".csv"):
  #   return send_file("stock/tmp/"+ code + ".csv")
  
  for root, dirs, files in os.walk(tmp_bin):
      for f in files:
          os.remove(os.path.join(root, f))
  get_historical_data(code)
  return send_file("stock/tmp/"+ code + ".csv")


