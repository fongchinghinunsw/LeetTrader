"""
    Export template for Complete usage guide and
    Learning knowledge about trading stocks
"""
import json
from flask import render_template, Blueprint

tutorial = Blueprint('tutorial', __name__)

@tutorial.route("/usage_guide", methods=['GET'])
def usage_guide():
  ''' Complete usage guide '''
  guides = json.loads(open('leettrader/tutorial/intents.json').read())
  usage_guide_str = ""
  
  # Title
  usage_guide_str += "<h1> Learn how to use LeetTrader </h1> <br>"
  # Body
  for tag in guides['guides']:
    # Context 1 is for tutorial on how to use LeetTrader
    if guides['context'] == 1:
      usage_guide_str += "<h3>" + tag + "</h3>" + "<br>" + "<p>" + tag['response'] + "</p>" + "<br>"

  return render_template('tutorial.html', usage_guide_str=usage_guide_str)


@tutorial.route("/help", methods=['GET'])
def help():
  ''' Learning knowledge about trading stocks '''
  trading = json.loads(open('leettrader/tutorial/intents.json').read())
  trading_help = ""
  # Title
  trading_help += "<h1> Learn trading terminology </h1> <br>"
  # Body
  for tag in trading['trading']:
    # Context 2 is for learning trading terminology.
    if trading['context'] == 2:
      trading_help += "<h3>" + tag + "</h3>" + "<br>" + "<p>" + tag['response'] + "</p>" + "<br>"
  return render_template('help.html', trading_help=trading_help)
