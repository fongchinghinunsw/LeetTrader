
'''
  This file helps to reset all investment records of a user.
'''

from flask_login import current_user
from leettrader import db
from leettrader.models import OwnStock, TransactionRecord

def reset_account(user=current_user):
  ''' Reset all investment records of user '''
  reset_bank(user)
  reset_owned_list(user)
  reset_record(user)


def reset_bank(user=current_user):
  ''' Reset the bank balance of user '''
  user.balance = {'AUD': 0.00, 'NZD': 0.00}
  db.session.commit()


def reset_owned_list(user=current_user):
  ''' Delete all owned stock of user '''
  uid = user.get_id()
  own_list = db.session.query(OwnStock).filter(OwnStock.user_id == uid).all()

  for item in own_list:
    db.session.delete(item)
  db.session.commit()


def reset_record(user=current_user):
  ''' Reset user's transaction records '''
  records = TransactionRecord.query.filter_by(
      user_id=user.get_id()).all()

  for record in records:
    db.session.delete(record)
  db.session.commit()