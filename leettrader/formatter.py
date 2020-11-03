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


def owned_table_item(name, code, qty, currency, market, purchase, pl):
  ''' Export a <tr> of stock info '''
  # Round market & purchase, then calculate the P/L
  worth = round(market, 4)
  paid = round(purchase, 4)

  # Format stock information
  own_stock = wrap_td(a_href(name, code))
  own_stock += wrap_td(str(qty))
  own_stock += wrap_td(str(worth))
  own_stock += wrap_td(str(paid))
  own_stock += wrap_td(color_span(pl))

  return wrap_tr(own_stock)


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


def wrap_tr(item):
  tag = '<tr style="padding: 10px 30px 10px 30px; border: 1px solid grey">'
  return tag + item + "</tr>"


def wrap_td(item):
  tag = '<td style="padding: 10px 30px 10px 30px; border: 1px, solid grey; text-align: center">'
  return tag + item + "</td>"


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

