from flask import render_template, request, redirect, url_for, Blueprint
from leettrader.models import Stock
from leettrader.stock.forms import SearchStockForm
from leettrader.stock.utils import get_search_result


stock = Blueprint('stock', __name__)

@stock.route('/search', methods=['GET', 'POST'])
def search_stock():
  """ Route the user to the search page if the stock code is correct
  """
  stock = SearchStockForm(request.form).stock.data
  code = stock.split()[-1].strip("()")
  if Stock.query.filter_by(code=code).first():
    return redirect(url_for('stock.search_page', code=code))

  return render_template('home.html')

@stock.route('/search/<string:code>')
def search_page(code):
  stock = Stock.query.filter_by(code=code).first()
  print(stock.code)
  result = get_search_result(stock.code)
  stock = f"{ stock.name } ({ stock.code })"
  
  if float(result['price_change']) == 0:
    color = "black"
  elif float(result['price_change']) > 0:
    color = "green"
  else:
    color = "red"

  print(result)

  return render_template('search_result.html', code=code, stock=stock, price=result['price'], price_change=result['price_change'], percent_change=result['percent_change'], color=color)