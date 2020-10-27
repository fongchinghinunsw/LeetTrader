"""
  This Module exports HTML formated contents
"""

def format_owned_info(name, qty, currency, market, purchase, pl):
  ''' Export a <div> of stock info '''
  # Round market & purchase, then calculate the P/L
  worth = round(market, 2)
  paid = round(purchase, 2)

  # Format stock information
  own_stock = '<b>' + name + '</b></br>'
  own_stock += " Qty: " + str(qty)
  own_stock += " | Currency: " + currency
  own_stock += " | Worth: " + str(worth)
  own_stock += " | Paid: " + str(paid)
  own_stock += " | P/L: " + color_span(pl) + '</br></br>'

  return "<div>" + own_stock + "</div>"



def color_span(num):
  if num >= 0:
    return '<span style="color: green"> +' + str(num) + '</span>'

  return '<span style="color: red"> +' + str(num) + '</span>'