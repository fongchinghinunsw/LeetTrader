'''
  Encapsulate information of balance sheet at home page:
    1. Stock list
    2. Total stock worth
    3. Bank balance
    4. Total = bank + total stock worth
  for both NZ and AU market.
'''

from flask_login import current_user
from leettrader.formatter import owned_table_item, color_span_2dp, format_bs


class BalanceSheet:
  '''
    Balance sheet class. API is as followed:
      1. update() - Update B/S by given stock
      2. get_final_bs() - Return final result
  '''
  def __init__(self):
    nz_bank = current_user.balance['NZD']
    au_bank = current_user.balance['AUD']
    self.stock_list = {'NZD': [], 'AUD': []}
    self.profit = {'NZD': 0.0, 'AUD': 0.0}
    self.stock_worth = {'NZD': 0.0, 'AUD': 0.0}
    self.bank = {'NZD': nz_bank, 'AUD': au_bank}
    self.color = {
        'NZD': False,
        'AUD': False
    }  # For format each row into diff colour

  def update(self, stock_info, purchase, qty):
    ''' Update B/S by inputing a new stock in owned list '''
    # Read information of the owned stock
    name = stock_info[0]
    code = stock_info[1]
    market = stock_info[2] * int(qty)
    currency = stock_info[3]

    # Calculate P/L & determine row color of the stock
    profit = round(market - purchase, 4)
    color = self.get_item_color(currency)

    # Format the result from above into HTML string
    item = owned_table_item(name, code, qty, market, purchase, profit, color)

    # Calcuate the new profit, worth, update stock list
    self.profit[currency] += profit
    self.stock_worth[currency] += market
    self.stock_list[currency].append(item)

  def get_final_bs(self):
    ''' Return B/S after calculation as formatted HTML String '''
    nz_table = self.get_stock_table('NZD')
    au_table = self.get_stock_table('AUD')
    bs_table = self.get_bs_table()

    return {'NZD': nz_table, 'AUD': au_table, 'BS': bs_table}

  def get_stock_table(self, currency):
    ''' Return a financial statement for a given market '''
    stocklist = self.stock_list[currency]
    profit = color_span_2dp(self.profit[currency])

    return {'list': stocklist, 'profit': profit}

  def get_bs_table(self):
    ''' Return a HTML formatted table of balance sheet '''
    nz_bank = color_span_2dp(self.bank['NZD'])
    nz_worth = color_span_2dp(self.stock_worth['NZD'])
    nz_tot = self.stock_worth['NZD'] + self.bank['NZD']
    nz_tot = color_span_2dp(nz_tot)

    au_bank = color_span_2dp(self.bank['AUD'])
    au_worth = color_span_2dp(self.stock_worth['AUD'])
    au_tot = self.stock_worth['AUD'] + self.bank['AUD']
    au_tot = color_span_2dp(au_tot)

    return format_bs(nz_bank, nz_worth, nz_tot, au_bank, au_worth, au_tot)

  def get_item_color(self, currency):
    ''' Determine the row color of owned stock list '''
    # Flip color for each row, return original color
    self.color[currency] = not self.color[currency]
    return not self.color[currency]
