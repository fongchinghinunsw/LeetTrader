#!/usr/bin/python3
"""
  run.py: create and start the flask server and inject Flask global template
  variables
"""

from leettrader import create_app
from leettrader.models import Stock
from leettrader.stock.forms import SearchStockForm
from flask_login import current_user
from flask import request, redirect, url_for
from flask_cors import CORS

app = create_app()
cors = CORS(app, resources={r"/search/<string:code>": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'


@app.context_processor
def inject_list_of_stocks():
  """ Inject the variable `stocks` in all the templates """
  stocks = Stock.query.all()
  stocks = [stock.name + " (" + stock.code + ")" for stock in stocks]
  return dict(stocks=stocks)


@app.context_processor
def inject_search_stock_form():
  """ Inject the search stock form """
  form = SearchStockForm()
  return dict(form=form)


@app.before_request
def check_admin():
  if request.path.startswith('/admin/'):
    if current_user.is_authenticated:
      if not current_user.is_admin():
        return redirect(url_for('users.home', userID=current_user.id))
    else:
      return redirect(url_for('main.landing'))


if __name__ == '__main__':
  app.app_context().push()
  app.run(debug=True)
