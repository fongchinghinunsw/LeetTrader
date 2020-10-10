from flask import render_template, request, Blueprint
from leettrader.stock.forms import SearchStockForm


stock = Blueprint('stock', __name__)

@stock.route('/search', methods=['GET', 'POST'])
def search_stock():
  print(SearchStockForm(request.form).stock.data)
  print("Reached")
  return render_template('search_page.html')