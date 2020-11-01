"""
    Export template for Complete usage guide and
    Learning knowledge about trading stocks
"""
import json
from flask import render_template, Blueprint

guide = Blueprint('guide', __name__)

@tutorial.route("/tutorial", methods=['GET'])
def tutorial():
  ''' Complete usage guide '''
  guides = json.loads(open('leettrader/tutorial/tutorial.json').read())
  usage_guide = ""
  ''' Title '''
  usage_guide += "<h1> Learn how to use LeetTrader </h1> <br>"
  ''' Body '''
  for tag in guides['guides']:
    usage_guide += "<h3>" + tag + "</h3>" + "<br>" + "<p>" + tag['response'] + "</p>" + "<br>"

  return render_template('tutorial.html', usage_guide=usage_guide)


@tutorial.route("/learntrading")
def help():
  ''' Learning knowledge about trading stocks '''
  guides = json.loads(open('leettrader/tutorial/trading.json').read())
  trading_help = ""
  ''' Title '''
  trading_help += "<h1> Learn trading terminology </h1> <br>"
  for tag in guides['guides']:
    trading_help += "<h3>" + tag + "</h3>" + "<br>" + "<p>" + tag['response'] + "</p>" + "<br>"
  return render_template('help.html', trading_help=trading_help)
