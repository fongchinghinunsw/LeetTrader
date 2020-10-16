'''
    Implementaiton of Class Diagram, with the following classes:
    1. User
    2. Watchlist
    3. Stock
    4. Transcation Record
    5. OwnStock
    6. ActionType
'''
import enum
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import PickleType
from flask_login import UserMixin
from leettrader import db, login_manager

watchlist_items = db.Table(
    'watchlist_items',
    db.Column('watchlist_id',
              db.Integer,
              db.ForeignKey('watchlist.id'),
              primary_key=True),
    db.Column('stock_id',
              db.Integer,
              db.ForeignKey('stock.id'),
              primary_key=True))
'''
  Relaod user by u_id stored in:
  https://flask-login.readthedocs.io/en/latest/
'''


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class UserType(enum.Enum):
  """ UserType class """
  ADMIN = 0
  NORMAL = 1


class User(db.Model, UserMixin):
  """ User class """
  # Attributes
  id = db.Column(db.Integer, primary_key=True)
  user_type = db.Column(db.Enum(UserType), nullable=False)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(30), nullable=False)
  balance = db.Column(MutableDict.as_mutable(PickleType),
                  default=dict())

  # backref is a way to declare a new property on the TransactionRecord class
  # You can then use transaction.person to get to the person at that address
  transactions = db.relationship('TransactionRecord',
                                 backref='user',
                                 lazy=True)
  own_stock = db.relationship('OwnStock', backref='user', lazy=True)
  watchlist = db.relationship('Watchlist',
                              backref='user',
                              lazy=True,
                              uselist=False)

  # Methods
  def __repr__(self):
    user = "User("
    user += "'{self.username}', '{self.email}', "
    user += "'{self.password}', '{self.balance}')"
    return user

  def getUserName(self):
    return self.username

  def get_id(self):
    return self.id


class Watchlist(db.Model):
  """Watchlist class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  date_added = db.Column(db.Date, nullable=False)
  stocks = db.relationship('Stock', secondary=watchlist_items, lazy=True)


class MarketType(enum.Enum):
  """ MarketType class"""
  NZ = 0
  AX = 1


class Stock(db.Model):
  """Stock class"""
  id = db.Column(db.Integer, primary_key=True)
  market_type = db.Column(db.Enum(MarketType), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  code = db.Column(db.String(20), nullable=False)
  ownstock_id = db.Column(db.Integer, db.ForeignKey('own_stock.id'))
  watchlist = db.relationship('Watchlist',
                              secondary=watchlist_items,
                              lazy=True)

  def __repr__(self):
    return f"Stock('{self.name}', '{self.code}')"

  def get_code(self):
    return self.code


class ActionType(enum.Enum):
  """ ActionType class"""
  BUY = 0
  SELL = 1


class TransactionRecord(db.Model):
  """ TransactionRecord class """
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  time = db.Column(db.DateTime, nullable=False)
  action = db.Column(db.Enum(ActionType), nullable=False)
  stock_id = db.Column(db.Integer, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  unit_price = db.Column(db.Float, nullable=False)


class OwnStock(db.Model):
  """ OwnStock class """
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  stock_id = db.Column(db.Integer, nullable=False)
  unit = db.Column(db.Integer, nullable=False)
  total_purchase_price = db.Column(db.Float, nullable=False)
  stock = db.relationship('Stock', lazy=True, uselist=False)
