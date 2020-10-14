"""
  Backend Utility Functions for Watchlist.
"""
from datetime import datetime
from leettrader import db
from leettrader.models import Watchlist, Stock


def add_stocks(current_user, code):
  """ Add stock to Watchlist """
  # Get Watchlist
  watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first()

  # If user does not have a watchlist, make a new one
  if watchlist is None:
    user_id = current_user.get_id()
    date_added = datetime.now()
    stocks = Stock.query.filter_by(code=code).first()
    watchlist = Watchlist(user_id=user_id,
                          date_added=date_added,
                          stocks=[stocks])
    db.session.add(watchlist)
    db.session.commit()


def remove_stocks(current_user, code):
  """ Remove stock from Watchlist """
  # Get Watchlist
  watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).filter(
      Watchlist.stocks.any(code=code)).first()

  # If watchlist is empty, delete watchlist in database
  if watchlist is not None:
    db.session.delete(watchlist)
    db.session.commit()


def get_list(current_user):
  ''' Return stock code & name of all stock in watchlist '''
  # Set up ans list and get watchlist of user
  ans_list = []
  watchlist = db.session.query(Watchlist).filter(
      Watchlist.user_id == current_user.get_id()).all()

  # Format of ansList: [code, name, code, name ...]
  for i in watchlist:
    ans_list.append(i.stocks[0].code)
    ans_list.append(i.stocks[0].name)
  return ans_list
