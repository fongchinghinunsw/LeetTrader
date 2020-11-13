from leettrader.stock.utils import get_currency_by_stock_code


def test_get_currency_by_stock_code(app):
  with app.app_context():
    assert get_currency_by_stock_code("ABA.NZ") == "NZD"
