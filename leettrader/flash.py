"""
  This Module exports strings for flash messages displayed.
"""


def build_order_success_msg(action, stock, unit):
  ''' Flash message after buy / sell stocks '''
  if action == "buy":
    flash_msg = "Brought " + stock + ". "
  else:
    flash_msg = "Sold " + stock + ". "

  return flash_msg + "You have " + str(unit) + " units of this stock remain."
