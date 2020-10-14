"""
  utils: contain all helper functions related to the watchlist
"""
from datetime import datetime
from leettrader import db
from leettrader.models import Watchlist, Stock


# Add stock to watchlist in db
def add_stocks(current_user, code):
  """
    add_stocks: add a stock to the user's watchlist
  """
  watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first()
  if watchlist is None:
    user_id = current_user.get_id()
    date_added = datetime.now()
    stocks = Stock.query.filter_by(code=code).first()
    watchlist = Watchlist(user_id=user_id,
                          date_added=date_added,
                          stocks=[stocks])
    db.session.add(watchlist)
    db.session.commit()


# Remove stock from watchlist in db
def remove_stocks(current_user, code):
  """
    remove_stocks: remove a stock to the user's watchlist
  """
  watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first()
  if watchlist is not None:
    db.session.delete(watchlist)
    db.session.commit()


def get_list(current_user):  #Flush watchlist on login
  """
    get a list of stocks in the user's watchlist in the format
    [stock_a_code, stock_a_name, stock_b_code, stock_b_name, ...]
  """
  codes = []
  watchlist = db.session.query(Watchlist).filter(
      Watchlist.user_id == current_user.get_id()).all()
  for i in watchlist:
    codes.append(i.stocks[0].code)
    codes.append(i.stocks[0].name)
  return codes
