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
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

SECRET_KEY = '7b0dff182c1a883a7c12855dcc6f411d'

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
  Reload user by u_id stored in:
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
  balance = db.Column(MutableDict.as_mutable(PickleType), default=dict())
  icon = db.Column(db.String(20), nullable=False, default='user.png')
  login_time = db.Column(db.DateTime)

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
    user += f"'{self.username}', '{self.email}', "
    user += f"'{self.password}', '{self.balance}', '{self.login_time}')"
    return user

  def getUserName(self):
    """ get the user name of the user """
    return self.username

  def get_id(self):
    """ get the id of the user """
    return self.id

  def get_time(self):
    """ get the login time of the user """
    return self.login_time

  def get_new_token(self, secs=1800):
    """  generate a new token  """
    # create a serializer with an expiration time of 1800s
    s = Serializer(SECRET_KEY, secs)
    # add the payload and create a token
    token = s.dumps({'user_id': self.get_id()}).decode('utf-8')
    return token

  @staticmethod
  def verify_reset_password_token(token):
    """  verify if the reset password token is correct """
    s = Serializer(SECRET_KEY)
    try:
      # check if the token is valid, try to load the token
      user_id = s.loads(token)['user_id']
    except:
      return None
    # return the user with user_id
    return User.query.get(user_id)

  @staticmethod
  def verify_confirmation_token(token):
    """  verify if the confirmation token is correct """
    s = Serializer(SECRET_KEY)
    try:
      # check if the token is valid, try to load the token
      user_id = s.loads(token)['user_id']
    except:
      return False
    return True

  @staticmethod
  def verify_delete_account_token(token):
    """  verify if the delete account token is correct """
    s = Serializer(SECRET_KEY)
    try:
      # check if the token is valid, try to load the token
      user_id = s.loads(token)['user_id']
    except:
      return None
    # return the user with user_id
    return User.query.get(user_id)

  def is_admin(self):
    return self.user_type == UserType.ADMIN


class Watchlist(db.Model):
  """Watchlist class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  date_added = db.Column(db.DateTime, nullable=False)
  stocks = db.relationship('Stock', secondary=watchlist_items, lazy=True)


class MarketType(enum.Enum):
  """ MarketType class"""
  NZ = 0
  AX = 1

  @staticmethod
  def get_market_labels():
    """ get fullname, area code of the markets """
    return [['New Zealand', 'nz'], ['Australia', 'au']]


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
  transaction_id = db.Column(db.Integer,
                             db.ForeignKey('transaction_record.id'))

  def __repr__(self):
    return f"Stock('{self.name}', '{self.code}')"

  def get_id(self):
    """ get id of the stock """
    return self.id

  def get_name(self):
    """ get name of the stock """
    return self.name

  def get_code(self):
    """ get code of the stock """
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
  stock = db.relationship('Stock', lazy=True, uselist=False)
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


class Reminder(db.Model):
  """ Reminder class """
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
  orig_price = db.Column(db.Float, nullable=False)
  target_price = db.Column(db.Float, nullable=False)

  def __repr__(self):
    reminder = "Reminder("
    reminder += f"'{self.user_id}', '{self.stock_id}', "
    reminder += f"'{self.orig_price}', '{self.target_price}')"
    return reminder

  @classmethod
  def get_reminders_by_user_id(cls, user_id):
    return cls.query.filter_by(user_id=user_id).all()

  def get_id(self):
    """ get id of the reminder """
    return self.id

  def get_user_id(self):
    """ get user id of the reminder """
    return self.user_id

  def get_stock_id(self):
    """ get stock id of the reminder """
    return self.stock_id

  def get_orig_price(self):
    """ get original price of the reminder """
    return self.orig_price

  def get_target_price(self):
    """ get target price of the reminder """
    return self.target_price
