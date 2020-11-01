"""
  This Module exports HTML formated contents
"""

def format_owned_info(name, code, qty, currency, market, purchase, pl):
  ''' Export a <div> of stock info '''
  # Round market & purchase, then calculate the P/L
  worth = round(market, 2)
  paid = round(purchase, 2)

  # Format stock information
  own_stock = '<b>' + a_href(name, code) + '</b></br>'
  own_stock += " Qty: " + str(qty)
  own_stock += " | Currency: " + currency
  own_stock += " | Worth: " + str(worth)
  own_stock += " | Paid: " + str(paid)
  own_stock += " | P/L: " + color_span(pl) + '</br></br>'

  return div(own_stock)


def format_watchlist_item(name, code, price, currency, change, percent):
  # Hyperlink & Stock Name
  ans = '<li id="' + code.replace(".", "_") + '"class="list-group-item list-group-item-light">'
  ans += a_href(str(name + ' (' + code + ')'), code)

  # Price Tags
  ans += '</br> Price: ' + str(price) + ' ' + currency
  ans += '</br> Price change: ' + color_span(change)
  ans += '</br> Percentage change: ' + color_span(percent) + '%</br>'
  ans += '</li>'

  return ans


def color_span(num):
  if num >= 0:
    return '<span style="color: green"> +' + str(num) + '</span>'

  return '<span style="color: red"> ' + str(num) + '</span>'


def div(content):
  return "<div>" + str(content) + "</div>"


def a_href(content, stockCode):
  url = '/search/' + stockCode
  
  ans = '<a href=' + url + '>'
  ans += str(content) + '</a>'

  return '<a href='+url+'>' + str(content) + '</a>'

