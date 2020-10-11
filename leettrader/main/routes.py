from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def landing():
  return render_template('landing.html')


@main.route("/<int:userID>")
def home(userID):
  return render_template('home.html')
