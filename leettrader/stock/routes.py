from flask import render_template, request, redirect, url_for, Blueprint
from leettrader.models import Stock, Watchlist, User
from leettrader.stock.forms import SearchStockForm
from leettrader.stock.utils import get_search_result
from flask_login import current_user, login_required

stock = Blueprint('stock', __name__)

@stock.route('/search', methods=['GET', 'POST'])
@login_required
def search_stock():
  """ Route the user to the search page if the stock code is correct
  """
  stock = SearchStockForm(request.form).stock.data
  code = stock.split()[-1].strip("()")
  if Stock.query.filter_by(code=code).first():
    return redirect(url_for('stock.search_page', code=code))

  return render_template('home.html')

@stock.route('/search/<string:code>')
@login_required
def search_page(code):
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
  
  ''' check if this stock is in the watch list, true if exists, otherwise false 
      user_id = current_user.user_id // after implemented user auth
  '''
  if Watchlist.query.filter_by(user_id = current_user.get_id()).filter(Watchlist.stocks.any(code=code)).first() == None:
    listed = False
  else: 
    listed = True


  return render_template('search_result.html', code=code, stock=stock, price=result['price'], price_change=result['price_change'], percent_change=result['percent_change'], color=color, listed=listed)