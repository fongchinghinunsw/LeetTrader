"""
  This Module exports HTML formated contents,
  which would be used to print the balance sheet at the HOME page.
"""


def format_bs(nz_bank, nz_worth, nz_tot, au_bank, au_worth, au_tot):
  ''' Export a formated table of Balance Sheet '''
  row_1 = '<tr class="ownedList-headers">'
  row_1 += '<th class="ownedList-header">'
  row_1 += '</th><th class="ownedList-header"> Bank </th>'
  row_1 += '<th class="ownedList-header"> Stock </th>'
  row_1 += '<th class="ownedList-header"> Total </th></tr>'

  row_2 = wrap_td("NZ Market") + wrap_td(nz_bank)
  row_2 += wrap_td(nz_worth) + wrap_td(nz_tot)
  row_2 = wrap_tr(row_2, False)

  row_3 = wrap_td("AU Market") + wrap_td(au_bank)
  row_3 += wrap_td(au_worth) + wrap_td(au_tot)
  row_3 = wrap_tr(row_3, True)

  return row_1 + row_2 + row_3


def owned_table_item(name, code, qty, market, purchase, pl, color):
  ''' Export a <tr> of stock info '''
  # Round market & purchase, then calculate the P/L
  worth = round(market, 2)
  paid = round(purchase, 2)

  # Format stock information
  own_stock = wrap_td(a_href(name, code))
  own_stock += wrap_td(str(qty))
  own_stock += wrap_td('{0:.2f}'.format(worth))
  own_stock += wrap_td('{0:.2f}'.format(paid))
  own_stock += wrap_td(color_span_2dp(pl))

  return wrap_tr(own_stock, color)


def format_watchlist_item(name, code, price, currency, change, percent):
  ''' Export HTML string of watchlist '''
  # Hyperlink & Stock Name
  ans = '<li id="' + code.replace(
    ".", "_") + '"class="list-group-item list-group-item-light">'
  ans += a_href(str(name + ' (' + code + ')'), code)

  # Price Tags
  ans += '</br> Price: ' + str(price) + ' ' + currency
  ans += '</br> Price change: ' + color_span_wl(change, False)
  ans += '</br> Percentage change: ' + color_span_wl(percent, True) + '</br>'
  ans += '</li>'

  return ans


def wrap_tr(item, color):
  ''' Wrap item with <tr> & set colour '''
  if color:
    tag = '<tr class="ownedList-row" style="background: #F5F5F5">'
  else:
    tag = '<tr class="ownedList-row">'

  return tag + item + "</tr>"


def wrap_td(item):
  tag = '<td class="ownedList-data">'
  return tag + item + "</td>"



def color_span_wl(num, percent):
  ans = str(num)
  if percent:
    ans += '%'

  if num == 0:
    return '<span> ' + ans + '</span>'

  if num > 0:
    return '<span style="color: green"> +' + ans + '</span>'

  return '<span style="color: red"> ' + ans + '</span>'



def color_span(num):
  if num == 0:
    return '<span> ' + str(num) + '</span>'

  if num > 0:
    return '<span style="color: green"> +' + str(num) + '</span>'

  return '<span style="color: red"> ' + str(num) + '</span>'


def color_span_2dp(num):
  if '{0:.2f}'.format(num) == "-0.00":
    return '<span style="color: green"> +0.00 </span>'

  if num > 0.0000:
    return '<span style="color: green"> +' + '{0:.2f}'.format(num) + '</span>'
  elif num < 0.0000:
    return '<span style="color: red"> ' + '{0:.2f}'.format(num) + '</span>'
  return '<span> ' + '{0:.2f}'.format(num) + '</span>'


def div(content):
  return "<div>" + str(content) + "</div>"


def a_href(content, stock_code):
  url = '/search/' + stock_code

  ans = '<a href=' + url + '>'
  ans += str(content) + '</a>'

  return '<a href=' + url + '>' + str(content) + '</a>'
