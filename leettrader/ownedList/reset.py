
'''
  This file helps to reset all investment records of a user.
'''

from flask_login import current_user
from leettrader import db
from leettrader.models import OwnStock, TransactionRecord, Reminder, Watchlist

def reset_account():
  ''' Reset all investment records of user '''
  reset_reminders()
  reset_bank()
  reset_owned_list()
  reset_record()

def delete_account_related():
  ''' delete all investment records of user '''
  reset_owned_list()
  reset_record()
  reset_reminders()
  delete_watchlist()


def reset_bank():
  ''' Reset the bank balance of user '''
  current_user.balance = {'AUD': 0.00, 'NZD': 0.00}
  db.session.commit()


def reset_owned_list():
  ''' Delete all owned stock of user '''
  uid = current_user.get_id()
  own_list = db.session.query(OwnStock).filter(OwnStock.user_id == uid).all()

  for item in own_list:
    db.session.delete(item)
  db.session.commit()


def reset_record():
  ''' Reset user's transaction records '''
  records = TransactionRecord.query.filter_by(
      user_id=current_user.get_id()).all()

  for record in records:
    db.session.delete(record)
  db.session.commit()


def reset_reminders():
  ''' Reset all the reminders set by user'''
  user_related_reminders = Reminder.query.filter_by(user_id=current_user.get_id()).all()
  for reminder in user_related_reminders:
    db.session.delete(reminder)
  db.session.commit()

def delete_watchlist():
  ''' delete all the watchlist set by user'''
  user_related_watchlist = Watchlist.query.filter_by(user_id=current_user.get_id()).all()
  for item in user_related_watchlist:
    db.session.delete(item)
  db.session.commit()
