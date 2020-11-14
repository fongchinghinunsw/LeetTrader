"""
  Utils: contain all helper functions for the project configuration
"""

import requests
from run import app
from leettrader import db, bcrypt
from leettrader.models import User, Stock


def create_db():
  """ Create the tables and database. """
  with app.app_context():
    db.create_all()


def drop_db():
  """ Delete the tables and database. """
  with app.app_context():
    db.drop_all()


def get_stocks_by_country(market):
  """ Get a list of stocks in a specified market. """
  return requests.get(
      f'https://finnhub.io/api/v1/stock/symbol?exchange={market}&token=bthb6v748v6v983blvg0'
  ).json()


def add_data():
  """ Add all the NZ stocks to the database. """
  markets = ['NZ', 'AX']
  with app.app_context():
    for market in markets:
      stocks = get_stocks_by_country(market)
      print(f"Adding {len(stocks)} stocks from the {market} market.")
      for stock in stocks:
        db.session.add(
            Stock(market_type=market,
                  name=stock['description'],
                  code=stock['symbol']))

    password_hashed = bcrypt.generate_password_hash("passw0rd").decode('utf-8')
    admin = User(user_type="ADMIN",
                 username="Donald Trump",
                 email="trump@leettrader.com",
                 password=password_hashed)
    db.session.add(admin)

    db.session.commit()
    admin = User(user_type="ADMIN",
                 username="Scomo",
                 email="scomo@leettrader.com",
                 password=password_hashed)
    db.session.add(admin)

    db.session.commit()


def init_db():
  drop_db()
  create_db()
  add_data()


init_db()
