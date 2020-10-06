import enum
from leettrader import db


class User(db.Model):
  """User class"""
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  balance = db.Column(db.Float, nullable=False)
  # backref is a way to declare a new property on the TransactionRecord class
  # You can then use transaction.person to get to the person at that address
  transactions = db.relationship('TransactionRecord', backref='user', lazy=True)
  own_stock = db.relationship('OwnStock', backref='user', lazy=True)
  watchlist = db.relationship('Watchlist', backref='user', lazy=True, uselist=False)

watchlist_items = db.Table('watchlist_items',
                  db.Column('watchlist_id', db.Integer, db.ForeignKey('watchlist.id'), primary_key=True),
                  db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)
                  )

  def getUserName():
    return self.username;


class Watchlist(db.Model):
  """Watchlist class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  date_added = db.Column(db.Date, nullable=False)
  stocks = db.relationship('Stock', secondary=watchlist_items, lazy=True)


class Stock(db.Model):
  """Stock class"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  code = db.Column(db.String(20), nullable=False)
  ownstock_id = db.Column(db.Integer, db.ForeignKey('own_stock.id'))
  watchlist = db.relationship('Watchlist', secondary=watchlist_items, lazy=True)


class ActionType(enum.Enum):
  """ActionType class"""
  BUY = 0
  SELL = 1


class TransactionRecord(db.Model):
  """TransactionRecord class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  time = db.Column(db.DateTime, nullable=False)
  action = db.Column(db.Enum(ActionType), nullable=False)
  stock_id = db.Column(db.Integer, nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  unit_price = db.Column(db.Float, nullable=False)


class OwnStock(db.Model):
  """OwnStock class"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  stock_id = db.Column(db.Integer, nullable=False)
  unit = db.Column(db.Integer, nullable=False)
  total_purchase_price = db.Column(db.Float, nullable=False)
  stock = db.relationship('Stock', lazy=True, uselist=False)