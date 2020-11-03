"""
  Export template for Landing & Home page
"""
from flask import render_template, Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route("/")
def landing():
  ''' Landing Page before Login '''
  return render_template('landing.html')


@main.route("/<int:userID>")
@login_required
def home(userID):
  ''' Home Page after Login '''
  
  return render_template('home.html')
