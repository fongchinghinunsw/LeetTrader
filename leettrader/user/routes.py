from flask import render_template, url_for, flash, redirect, Blueprint
from leettrader.main.forms import LoginForm, RegisterForm
from leettrader.models import User
from leettrader import db
from flask_login import login_user, logout_user, current_user, login_required

user = Blueprint('user', __name__)


@user.route("/<int:userID>")
def home(userID):
  return render_template('home.html')


@user.route("/register", methods=['GET', 'POST'])
def register():
  rform = RegisterForm()
  if rform.validate_on_submit():
    user = User(username=rform.username.data, email=rform.email.data, password=rform.password.data, balance=0)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('user.login'))
  return render_template('register.html', title='register', form=rform)


@user.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  login_form = LoginForm()
  if login_form.validate_on_submit():
    user = User.query.filter_by(email=login_form.email.data).first()
    if user and user.password == login_form.password.data:
      login_user(user, remember=login_form.remember.data)
      return redirect(url_for('user.home', userID=user.id))
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
