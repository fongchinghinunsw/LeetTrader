from flask import Flask, render_template, url_for, flash, redirect, Blueprint
from leettrader.main.forms import LoginForm, RegisterForm
from leettrader.models import User
from leettrader import db

main = Blueprint('main', __name__)

@main.route("/")
def home():
  return render_template('landing.html')

@main.route("/register", methods=['GET', 'POST'])
def register():
  rform = RegisterForm()
  if rform.validate_on_submit:
    print('sd')
  #   user = User(username=rform.username.data, email=rform.email.data, password=rform, balance=1000000.0)
  #   db.session.add(user)
  #   db.session.commit()
  #   return redirect(url_for('login'))
  return render_template('register.html', title='register', form=rform)

@main.route("/login", methods=['GET', 'POST'])
def login():
  login_form = LoginForm()
  return render_template('login.html', title='login', form=login_form)





