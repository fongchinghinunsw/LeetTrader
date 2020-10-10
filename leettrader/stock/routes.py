from flask import render_template, request, redirect, url_for, Blueprint
from leettrader.models import Stock
from leettrader.stock.forms import SearchStockForm


stock = Blueprint('stock', __name__)

@stock.route('/search', methods=['GET', 'POST'])
def search_stock():
  stock = SearchStockForm(request.form).stock.data
  code = stock.split()[-1].strip("()")
  if Stock.query.filter_by(code=code).first():
    return redirect(url_for('stock.search_page', code=code))

  return render_template('home.html')

@stock.route('/<string:code>', methods=['GET', 'POST'])
def search_page(code):
  stock = Stock.query.filter_by(code=code).first()
  stock = f"{ stock.name } ({ stock.code})"
  return render_template('search_page.html', stock=stock)