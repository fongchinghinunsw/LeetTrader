from flask import render_template, url_for, flash, redirect, Blueprint
from leettrader.user.forms import LoginForm, RegisterForm
from leettrader.models import User
from leettrader import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

user = Blueprint('user', __name__)

@user.route("/home")
def home():
  return render_template('home.html')

@user.route("/register", methods=['GET', 'POST'])
def register():
  rform = RegisterForm()
  if rform.validate_on_submit():
    password_hashed = bcrypt.generate_password_hash(rform.password.data).decode('utf-8')
    user = User(username=rform.username.data, email=rform.email.data, password=password_hashed, balance=0)
    db.session.add(user)
    db.session.commit()
    flash('Account created successfully, please login !', 'success')
    return redirect(url_for('user.login'))
  return render_template('register.html', title='register', form=rform)


@user.route("/login", methods=['GET', 'POST'])
def login():
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = User.query.filter_by(email=login_form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, login_form.password.data):
      login_user(user, remember=login_form.remember.data)
      return redirect(url_for('user.home', userID=user.id))
    elif not user:
      flash('This email has not been registered yet', 'danger')
    else:
      flash('Wrong password, please try again', 'danger')
      
  return render_template('login.html', title='login', form=login_form)

@user.route("/settings")
@login_required
def settings():
  pass

@user.route("/logout", methods=['GET', 'POST'])
def logout():
  logout_user()
  return redirect(url_for('main.landing'))
