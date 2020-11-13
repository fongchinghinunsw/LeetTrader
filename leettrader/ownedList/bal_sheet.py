from flask_login import current_user
from leettrader.formatter import owned_table_item, color_span_2dp

class BalanceSheet:
  def __init__(self):
    nz_bank = current_user.balance['NZD']
    au_bank = current_user.balance['AUD']
    self.stock_list = {'NZD': [], 'AUD': []}
    self.profit = {'NZD': 0.0, 'AUD': 0.0}
    self.stock_worth = {'NZD': 0.0, 'AUD': 0.0}
    self.bank = {'NZD': nz_bank, 'AUD': au_bank}


  def update(self, stock_info, purchase, NZisColorGrey, AUisColorGrey, qty):
    name = stock_info[0]
    code = stock_info[1]
    market = stock_info[2] * int(qty)
    currency = stock_info[3]

    profit = round(market-purchase, 4)
    item = owned_table_item(name, code, qty, currency, market, purchase, profit, NZisColorGrey)
    NZisColorGrey = True if False else True
    self.profit[currency] += profit
    self.stock_worth[currency] += purchase
    self.stock_list[currency].append(item)


  def get_final_bs(self):
    nz_statement = self.get_statement('NZD')
    au_statement = self.get_statement('AUD')
    return {'NZD': nz_statement, 'AUD': au_statement}


  def get_statement(self, currency):
    stocklist = self.stock_list[currency]
    bank = color_span_2dp(self.bank[currency])
    profit = color_span_2dp(self.profit[currency])
    worth = color_span_2dp(self.stock_worth[currency])
    
    tot = self.stock_worth[currency] + self.bank[currency]
    total = color_span_2dp(tot)

    return {'list': stocklist, 'bank': bank, 'profit': profit, 'worth': worth, 'total': total}
