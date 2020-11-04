from threading import Condition, Thread
from time import sleep

from flask import has_app_context
from leettrader import db
from leettrader.user.send_emails import send_stock_reminder
from leettrader.stock.utils import get_search_result
from leettrader.models import User, Stock, Reminder

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

