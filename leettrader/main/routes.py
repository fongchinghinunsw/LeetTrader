from flask import Flask, render_template, url_for, flash, redirect
from leettrader.main.forms import LoginForm, RegisterForm
from leettrader.models import User
from leettrader import app, db
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def home():
  return render_template('landing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  rform = RegisterForm()
  if rform.validate_on_submit():
    user = User(username=rform.username.data, email=rform.email.data, password=rform.password.data, balance=0)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('register.html', title='register', form=rform)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user_db = User.query.filter_by(email=login_form.email.data).first()
    if user_db and user_db.password == login_form.password.data:
      login_user(user_db, remember=login_form.remember.data)
      return redirect(url_for('afterLogin'))
    
  return render_template('login.html', title='login', form=login_form)

@app.route("/settings")
@login_required
def settings():
  pass

@app.route("/logout", methods=['GET', 'POST'])
def logout():
  logout_user()
  return redirect(url_for('home'))

# just for testing after successful login
@app.route("/afterLogin", methods=['GET', 'POST'])
def afterLogin():
  return render_template('afterLogin.html', title='login')


