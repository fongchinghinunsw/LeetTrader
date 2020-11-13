from threading import Condition, Thread
from time import sleep
from datetime import datetime

from flask import has_app_context
from leettrader import db
from leettrader.user.send_emails import send_stock_reminder
from leettrader.stock.utils import get_search_result
from leettrader.models import User, Stock, Reminder, TransactionRecord, OwnStock
from flask_login import current_user



def trade_stock(ownStock, sid, unit_change, price_change, action):
  # Calculate change of price and unit
  if action == "sell":
      unit_change *= -1
      price_change *= -1

  # Buy Stock at first time
  if ownStock is None:
      ownStock = OwnStock(user_id=current_user.get_id(), stock_id=sid,
                          unit=unit_change, total_purchase_price=price_change)
      db.session.add(ownStock)

  # Buy Stock / Sell Stock
  else:
    ownStock.unit += unit_change
    ownStock.total_purchase_price += price_change
    if ownStock.unit == 0:
      db.session.delete(ownStock) # Delete Tuple if Ownstock is Zero

  db.session.commit()


def create_transaction_record(action, uid, stock_obj, stock_id, quantity, checkout_form):
  action = {"buy": "BUY", "sell": "SELL"}[action]
  print(stock_obj, "-----------------")
  record = TransactionRecord(user_id=current_user.get_id(), 
                              time=datetime.now(), action=action, 
                              stock=stock_obj, stock_id=stock_id, 
                              quantity=quantity, unit_price=checkout_form.data['current_market_price'])
  db.session.add(record)
  db.session.commit()



def add_and_start_reminder(reminder, username):

  thread = Thread(name="ReminderHandler", target=reminder_handler, args=[reminder, username])
  thread.daemon = True
  thread.start()

def reminder_handler(reminder, username):

  from leettrader import create_app
  app = create_app()


  with app.app_context():
    db.session.add(reminder)
    db.session.commit()

    reminder_id = reminder.get_id()
    print("Reminder is", reminder)
    print("Reminder id is", reminder_id, "right after initialized")
    stock_id = reminder.get_stock_id()
    orig_price = float(reminder.orig_price)
    target_price = float(reminder.target_price)

    print(Reminder.query.all())

    user = User.query.filter_by(username=username).first()
    stock = Stock.query.filter_by(id=stock_id).first()
    print(stock.get_code(), "within the handler", flush=True)

    # is the reminder still existing? (has it been deleted?)
    exists = True
    print("Reminder id is", reminder_id)
    print(Reminder.query.filter_by(id=reminder_id).all(), "is the reminders list")
    if orig_price < target_price:
      while True and exists:  
        if not exists:
          print("Not exist")
        current_price = float(get_search_result(stock.get_code())['price'])
        if current_price >= target_price:
          print(reminder, "hits the price, thread stopped")
          send_stock_reminder(user, stock, reminder, current_price)
          break
        print(reminder, "sleeps for 10 seconds...")
        sleep(10)
        exists = False if Reminder.query.filter_by(id=reminder_id).all() == [] else True
    else:
      while True and exists:  
        if not exists:
          print("Not exist")
        current_price = float(get_search_result(stock.get_code())['price'])
        if current_price <= target_price:
          print(reminder, "hits the price, thread stopped")
          send_stock_reminder(user, stock, reminder, current_price)
          break
        print(reminder, "sleeps for 10 seconds...")
        sleep(10)
        exists = False if Reminder.query.filter_by(id=reminder_id).all() == [] else True

    if exists:
      db.session.delete(reminder)
      db.session.commit()
    else:
      print("The reminder is deleted manually")

