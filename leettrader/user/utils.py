from threading import Condition, Thread
from time import sleep

from flask import has_app_context
from leettrader.stock.utils import get_search_result
from leettrader.models import User

def add_and_start_reminder(reminder):
  thread = Thread(name="ReminderHandler", target=reminder_handler, args=[reminder])
  thread.daemon = True
  thread.start()

def reminder_handler(reminder):
  stock_code = reminder.stock_id
  orig_price = float(reminder.orig_price)
  target_price = float(reminder.target_price)

  from leettrader import create_app
  app = create_app()

  with app.app_context():
    print(User.query.all())
    if orig_price < target_price:
      while True:  
        current_price = float(get_search_result(stock_code)['price'])
        if current_price >= target_price:
          print("Hit the price, thread stopped")
          break
        sleep(5)
        print("sleep for 5 seconds...")
    else:
      while True:
        current_price = float(get_search_result(stock_code)['price'])
        if current_price <= target_price:
          print("Hit the price, thread stopped")
          break
        sleep(5)
        print("sleep for 5 seconds...")
