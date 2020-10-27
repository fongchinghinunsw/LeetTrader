from threading import Condition, Thread
from time import sleep

from leettrader.stock.utils import get_search_result

def add_and_start_reminder(reminder):
  thread = Thread(name="ReminderHandler", target=reminder_handler, args=[reminder])
  thread.daemon = True
  thread.start()

def reminder_handler(reminder):
  stock_code = reminder.stock_id
  orig_price = reminder.orig_price
  target_price = reminder.target_price
  if orig_price < target_price:
    while True:  
      current_price = get_search_result(stock_code)
      if current_price >= target_price:
        print("Hit the price, thread stopped")
        break
      sleep(5)
      print("sleep for 5 seconds...")
  else:
    while True:
      current_price = get_search_result(stock_code)
      if current_price <= target_price:
        print("Hit the price, thread stopped")
        break
      sleep(5)
      print("sleep for 5 seconds...")
