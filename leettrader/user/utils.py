from threading import Condition, Thread
from time import sleep

from flask import has_app_context
from leettrader.user.send_emails import send_stock_reminder
from leettrader.stock.utils import get_search_result
from leettrader.models import User

def add_and_start_reminder(reminder, username):
  thread = Thread(name="ReminderHandler", target=reminder_handler, args=[reminder, username])
  thread.daemon = True
  thread.start()

def reminder_handler(reminder, username):
  stock_code = reminder.stock_id
  orig_price = float(reminder.orig_price)
  target_price = float(reminder.target_price)

  from leettrader import create_app
  app = create_app()

  with app.app_context():
    user = User.query.filter_by(username=username).first()
    print(user)
    if orig_price < target_price:
      while True:  
        current_price = float(get_search_result(stock_code)['price'])
        if current_price >= target_price:
          print("Hit the price, thread stopped")
          send_stock_reminder(user)
          break
        sleep(5)
        print("sleep for 5 seconds...")
    else:
      while True:
        current_price = float(get_search_result(stock_code)['price'])
        if current_price <= target_price:
          print("Hit the price, thread stopped")
          send_stock_reminder(user)
          break
        sleep(5)
        print("sleep for 5 seconds...")
