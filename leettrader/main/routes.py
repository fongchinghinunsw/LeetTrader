"""
  Export template for Landing & Home page
"""
from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
def landing():
  ''' Landing Page before Login '''
  return render_template('landing.html')
