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
  # Get content from the JSON file which contains the tutorial.
  guides = json.loads(open('leettrader/tutorial/intents.json').read())
  usage_guide_str = ""
  
  # Title
  usage_guide_str += "<br><h1> Learn how to use LeetTrader </h1> <br>"
  # Body
  for intent in guides['intents']:
    # Context 1 is for tutorial on how to use LeetTrader
    if intent['context'] == 1:
      usage_guide_str += "<h3>" + intent['tag'] + "</h3>" + "<br>" + "<p>" + intent['responses'][0] + "</p>" + "<br>"

  return render_template('usage_guide.html', usage_guide_str=usage_guide_str)


@tutorial.route("/tutorial", methods=['GET'])
def help():
  ''' Learning knowledge about trading stocks '''
  # Get content from the JSON file which contains the tutorial.
  trading = json.loads(open('leettrader/tutorial/intents.json').read())
  trading_help = ""
  # Title
  trading_help += "<br><h1> Learn trading terminology </h1> <br>"
  # Body
  for intent in trading['intents']:
    # Context 2 is for learning trading terminology.
    if intent['context'] == 2:
      trading_help += "<h3>" + intent['tag'] + "</h3>" + "<br>" + "<p>" + intent['responses'][0] + "</p>" + "<br>"
  return render_template('tutorial.html', trading_help=trading_help)
