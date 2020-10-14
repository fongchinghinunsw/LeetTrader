"""
  Routing of Search Page
"""

from flask import render_template, request, redirect, url_for, Blueprint
from leettrader.models import Stock, Watchlist
from leettrader.stock.forms import SearchStockForm
from leettrader.stock.utils import get_search_result
from flask_login import current_user, login_required

stock = Blueprint('stock', __name__)


@stock.route('/search', methods=['GET', 'POST'])
@login_required
def search_stock():
  ''' Check stock code, direct to Search Page '''
  # Get stock code
  stock_input = SearchStockForm(request.form).stock.data
  code = stock_input.split()[-1].strip("()")

  # Go to search page if stock code is valid, home page otherwise
  if Stock.query.filter_by(code=code).first():
    return redirect(url_for('stock.search_page', code=code))

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

  if float(result['price_change']) == 0:
    color = "black"
  elif float(result['price_change']) > 0:
    color = "green"
  else:
    color = "red"
  print(result)

  # Check if stock is already in watchlist
  if Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first() is None:
    listed = False
  else:
    listed = True


  # Export "search_result.html" from template, passing in:
    # 1. Stock code & name
    # 2. Stock price, price changes
    # 3. Colour of label of price information
    # 4. Whether stock is already in stocklist
  return render_template('search_result.html',
                         code=code,
                         stock=stock,
                         price=result['price'],
                         price_change=result['price_change'],
                         percent_change=result['percent_change'],
                         color=color,
                         listed=listed)
