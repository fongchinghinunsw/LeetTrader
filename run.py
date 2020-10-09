from leettrader import create_app
from leettrader.models import Stock

app = create_app()

@app.context_processor
def inject_list_of_stocks():
  """ Inject the variable `stock` in all the templates """
  stocks = Stock.query.all()
  stocks = [stock.name + " " + stock.code for stock in stocks]
  return dict(stocks=stocks)

if __name__ == '__main__':
  app.run(debug=True)