from flask import render_template, request, redirect, url_for, Blueprint
from datetime import datetime
from leettrader import db
from leettrader.models import User, Watchlist, Stock
#from leettrader.stock.utils import get_search_result
from flask_login import current_user

def add_stocks(current_user, code):
    watchlist = Watchlist.query.filter_by(user_id = current_user.get_id()).filter(Watchlist.stocks.any(code=code)).first()
    if watchlist is None:
        user_id = current_user.get_id()
        print(user_id)
        date_added = datetime.now()
        stocks = Stock.query.filter_by(code=code).first()
        print(stocks)
        watchlist = Watchlist(user_id = user_id, date_added = date_added, stocks = [stocks])
        db.session.add(watchlist)
        db.session.commit()

def remove_stocks(current_user, code):
    user_id = current_user.get_id()
    stocks = Stock.query.filter_by(code=code).first()
    watchlist = Watchlist.query.filter_by(user_id = current_user.get_id()).filter(Watchlist.stocks.any(code=code)).first()
    if watchlist is not None:
        db.session.delete(watchlist)
        db.session.commit()
    
def get_list(current_user): #Flush watchlist on login
    codes = []
    watchlist = db.session.query(Watchlist).filter(Watchlist.user_id == current_user.get_id()).all()
    for i in watchlist:
        codes.append(i.stocks[0].code)
    return codes
    