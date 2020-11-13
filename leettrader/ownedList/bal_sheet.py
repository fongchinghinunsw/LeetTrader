'''
  Encapsulate information of balance sheet at home page:
    1. Stock list
    2. Total stock worth
    3. Bank balance
    4. Total = bank + total stock worth
  for both NZ and AU market.
'''

from flask_login import current_user
from leettrader.formatter import owned_table_item, color_span_2dp


class BalanceSheet:
  '''
    Balance sheet class
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

  def update(self, stock_info, purchase, qty):
    ''' Update B/S by inputing a new stock in owned list '''
    name = stock_info[0]
    code = stock_info[1]
    market = stock_info[2] * int(qty)
    currency = stock_info[3]

    profit = round(market - purchase, 4)
    item = owned_table_item(name, code, qty, currency, market, purchase,
                            profit, False)

    self.profit[currency] += profit
    self.stock_worth[currency] += purchase
    self.stock_list[currency].append(item)


  def get_final_bs(self):
    ''' Return B/S after calculation as formatted HTML String '''
    nz_statement = self.get_statement('NZD')
    au_statement = self.get_statement('AUD')
    return {'NZD': nz_statement, 'AUD': au_statement}


  def get_statement(self, currency):
    ''' Return a financial statement for a given market '''
    stocklist = self.stock_list[currency]
    bank = color_span_2dp(self.bank[currency])
    profit = color_span_2dp(self.profit[currency])
    worth = color_span_2dp(self.stock_worth[currency])

    tot = self.stock_worth[currency] + self.bank[currency]
    total = color_span_2dp(tot)

    return {
        'list': stocklist,
        'bank': bank,
        'profit': profit,
        'worth': worth,
        'total': total
    }
