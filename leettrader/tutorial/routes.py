"""
    Export template for Complete usage guide and
    Learning knowledge about trading stocks
"""
import json
from flask import render_template, Blueprint

guide = Blueprint('guide', __name__)

@guide.route("/help", methods=['GET'])
def help():
  ''' Complete usage guide '''
  guides = json.loads(open('leettrader/guide/tutorial.json').read())
  usage_guide = ""
  for tag in guides['guides']:
    usage_guide += "<h3>" + tag + "</h3>" + "<br>" + "<p>" + tag['response'] + "</p>" + "<br>"

  return render_template('help.html', usage_guide=usage_guide)

"""
@main.route("/learntrading")
def learn_trading(userID):
  ''' Learning knowledge about trading stocks '''
  return render_template('learntrading.html')
"""