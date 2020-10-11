from leettrader import create_app
from leettrader.models import Stock
from leettrader.stock.forms import SearchStockForm

app = create_app()

@app.context_processor
def inject_list_of_stocks():
  """ Inject the variable `stocks` in all the templates """
  stocks = Stock.query.all()
  stocks = [stock.name + " (" + stock.code + ")" for stock in stocks]
  return dict(stocks=stocks)

@app.context_processor
def inject_search_stock_form():
  form = SearchStockForm()
  return dict(form=form)


if __name__ == '__main__':
  app.run(debug=True)