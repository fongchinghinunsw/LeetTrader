"""
  Backend Utility Functions for Watchlist.
"""
from datetime import datetime
from leettrader import db
from leettrader.models import Watchlist, Stock
from leettrader.stock.utils import get_search_result
from leettrader.formatter import format_watchlist_item


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

  # For each item in watchlist, format it into HTML Tags
  for i in watchlist:
    name = i.stocks[0].name
    code = i.stocks[0].code

    # Search stock & get prices
    search_result = get_search_result(code)
    price = float(search_result['price'])
    change = search_result['price_change']
    percent = search_result['percent_change']

    # Cast to float (2 d.p.)
    price = round(float(price), 2)
    change = str_to_float(change)
    percent = str_to_float(percent)

    # Format all information to HTML tag string
    item = format_watchlist_item(name, code, price, change, percent)
    ans_list.append(item)

  return ans_list


def str_to_float(num):
  ''' Convert a string into a 2 d.p. float '''
  if num[-1] == '%':
    return str_to_float(num[:-1])

  if num[0] == '-':
    return str_to_float(num[1:])

  return round(float(num), 2)
