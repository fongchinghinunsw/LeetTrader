"""
  Routing of Account Mangement, Simul-Buy and Sell
"""
from flask import render_template, url_for, flash, redirect, Blueprint

from leettrader.user.forms import (LoginForm, RegisterForm, resetRequestForm,
resetPasswordForm, deleteRequestForm, OrderForm, CheckoutForm)

from leettrader.stock.utils import get_search_result
from leettrader.models import User, Stock, OwnStock
from leettrader import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

user = Blueprint('user', __name__)

# ugly global variable for now
new_username = None
new_email = None
new_password = None


# Use flask-mail to send the email
def send_confirmation_email(new_user):
  # get a new token and start timer !
  token = new_user.get_new_token()
  msg = Message('Confirmation for new account', sender='leettrader2020@gmail.com', recipients=[new_user.email])
  msg.body = f'''Dear {new_user.username}, to confirm your email and activate your new account, please click the link below:
{url_for('user.confirm', token=token, _external=True)}

If you did not create a new account, please just ignore this email.

Cheers,
LeetTrader Team
  '''
  mail.send(msg)


# Use flask-mail to send the email
def send_reset_password_email(user):
  # get a new token and start timer !
  token = user.get_new_token()
  msg = Message('Password reset request', sender='leettrader2020@gmail.com', recipients=[user.email])
  msg.body = f'''Dear {user.username}, to reset your password, please click the link below:
{url_for('user.', token=token, _external=True)}

If you did not make the request, please just ignore this email.

Cheers,
LeetTrader Team
  '''
  mail.send(msg)

# Use flask-mail to send the email
def send_delete_account_email(user):
  # get a new token and start timer !
  token = user.get_new_token()
  msg = Message('Delete the account', sender='leettrader2020@gmail.com', recipients=[user.email])
  msg.body = f'''Dear {user.username}, to cancel your account, please click the link below:
{url_for('user.delete_account_token', token=token, _external=True)}
Please be aware that all your account information and data will be deleted and cannot be retrieved.

If you did not make the request, please just ignore this email.

Cheers,
LeetTrader Team
  '''
  mail.send(msg)


@user.route("/home")
@login_required
def home():
  ''' Home Page '''
  return render_template('home.html')


@user.route("/register", methods=['GET', 'POST'])
def register():
  ''' Register Page '''
  # Set up register form
  rform = RegisterForm()

  # Create account when click on submit button
  if rform.validate_on_submit():
    # Hash password & Read User Input
    password_hashed = bcrypt.generate_password_hash(
        rform.password.data).decode('utf-8')
    new_user = User(user_type = "NORMAL",
                username=rform.username.data,
                email=rform.email.data,
                password=password_hashed)

    global new_username
    new_username = new_user.username
    global new_email
    new_email = new_user.email
    global new_password
    new_password = new_user.password

    # send the confirmation email
    send_confirmation_email(new_user)
    flash('Confirmation email has been sent, please check your emails', 'info')
    return redirect(url_for('user.login'))
  return render_template('register.html', title='register', form=rform)

@user.route("/confirm/<token>", methods=['GET', 'POST'])
@login_required
def confirm(token):
  # check if the token is valid
  res = User.verify_confirmation_token(token)
  if res is False:
    flash('The token has expired !', 'warning')
    return redirect(url_for('user.register'))
  else:
    # Push changes to database, go to Login page
    new_user = User(user_type = "NORMAL",
                username=new_username,
                email=new_email,
                password=new_password)
    db.session.add(new_user)
    db.session.commit()
    flash('Account created successfully, please login !', 'success')
    return redirect(url_for('user.login'))


@user.route("/login", methods=['GET', 'POST'])
def login():

  login_form = LoginForm()

  # When click login, read user inputs 
  if login_form.validate_on_submit():
    user = User.query.filter_by(email=login_form.email.data).first()

    # If both Email & Password are correct, go to Home Page
    if user and bcrypt.check_password_hash(user.password,
                                           login_form.password.data):
      login_user(user, remember=login_form.remember.data)
      return redirect(url_for('user.home', userID=user.id))

    # Show Error message otherwise
    elif not user:
      flash('This email has not been registered yet', 'danger')
    else:
      flash('Wrong password, please try again', 'danger')

  # Fail to login, stay in login page
  return render_template('login.html', title='login', form=login_form)


@user.route("/settings")
@login_required
def settings():
  ''' TO_DO '''
  pass


@user.route("/logout", methods=['GET', 'POST'])
def logout():
  
  logout_user()
  return redirect(url_for('main.landing'))



@user.route("/resetPassword", methods=['GET', 'POST'])
def reset_request():
  # if current_user.is_authenticated:
  #   return redirect(url_for('user.home'))
  form = resetRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    # print('sending')
    send_reset_password_email(user)
    flash('An email has been sent to reset your password', 'info')
    return redirect(url_for('user.login'))
  return render_template('reset_request.html', title='reset password', form=form)


@user.route("/resetPassword/<token>", methods=['GET', 'POST'])
# reset their password when the token is active
def reset_password_token(token):
  # if current_user.is_authenticated:
  #   return redirect(url_for('user.home'))
  # check if the token is valid
  user = User.verify_reset_password_token(token)
  if user is None:
    flash('The token has expired !', 'warning')
    return redirect(url_for('user.reset_request'))
  else:
    form = resetPasswordForm()
    if form.validate_on_submit():
      # Hash password & Read User Input
      password_hashed = bcrypt.generate_password_hash(
          form.password.data).decode('utf-8')
      user.password = password_hashed
      db.session.commit()
      flash('Account has been reset, please login !', 'success')
      return redirect(url_for('user.login'))
    return render_template('reset_password_token.html', title='reset password', form=form)

# delete account 
@user.route("/deleteRequest", methods=['GET', 'POST'])
@login_required
def deleteRequest():
  # if current_user.is_authenticated:
  #   return redirect(url_for('user.home'))
  form = deleteRequestForm()

  if form.validate_on_submit():
    if form.email.data != current_user.email:
      flash('This is not the email for your account, please try again', 'danger')
      return render_template('delete_request.html', title='Delete your account', delete_form=form)
      
    # user = User.query.filter_by(email=form.email.data).first()
    # # print(user)

    if bcrypt.check_password_hash(current_user.password, form.password.data):
      curr_user = User.query.filter_by(email=form.email.data).first()
      send_delete_account_email(curr_user)
      flash('An email has been sent to cancel your account', 'info')
      logout_user()
      return redirect(url_for('user.login'))
    else:
      flash('Wrong password, please try again', 'danger')

  return render_template('delete_request.html', title='Delete your account', delete_form=form)


@user.route("/deleteRequest/<token>", methods=['GET', 'POST'])
# reset their password when the token is active
def delete_account_token(token):
  # check if the token is valid
  user = User.verify_delete_account_token(token)
  if user is None:
    flash('The token has expired !', 'warning')
    return redirect(url_for('user.deleteRequest'))
  else:
    # do the deletion if the token is valid
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted successfully', 'success')
    return redirect(url_for('main.landing'))


@user.route("/order/<string:action>/<string:stock>", methods=['GET', 'POST'])
@login_required
def order(stock, action):
  ''' Order Page '''
  order_form = OrderForm()
  
  if order_form.validate_on_submit():
    quantity = order_form.quantity.data

    stock_id = Stock.query.filter_by(code=stock).first().id
    print(stock_id)

    if action == "buy":
      print("You are buying a stock")
      return redirect(
          url_for('user.checkout',
                  action=action,
                  stock=stock,
                  quantity=quantity))

    elif action == "sell":
      ownStock = OwnStock.query.filter_by(user_id=current_user.get_id(),
                                          stock_id=stock_id).first()
      print("You don't own any this stock")
      if ownStock is not None and ownStock.unit >= quantity:
        print("Currently, you own", ownStock.unit, "units of stock")
        return redirect(
            url_for('user.checkout',
                    action=action,
                    stock=stock,
                    quantity=quantity))
      else:
        flash('You do not have enough amount of this stock to sell', "danger")

  return render_template('order.html',
                         title='order',
                         stock=stock,
                         action=action,
                         order_form=order_form)


@user.route("/checkout/<string:action>/<string:stock>/<quantity>",
            methods=['GET', 'POST'])
@login_required
def checkout(stock, action, quantity):
  stock_obj = Stock.query.filter_by(code=stock).first()
  stock_id = stock_obj.id

  current_market_price = get_search_result(stock_obj.code)['price']

  checkout_form = CheckoutForm(
      current_market_price=current_market_price,
      total_price=str(float(current_market_price) * int(quantity)))
  if checkout_form.validate_on_submit():
    # the submit button is clicked.
    if checkout_form.submit.data:
      ownStock = OwnStock.query.filter_by(user_id=current_user.get_id(),
                                          stock_id=stock_id).first()
      if ownStock is None:
        # only true if the action is buy.
        ownStock = OwnStock(user_id=current_user.get_id(),
                            stock_id=stock_id,
                            unit=int(quantity),
                            total_purchase_price=int(quantity) *
                            float(checkout_form.data['current_market_price']))
        # "success" is bootstrap green alert formatting - checkout bootstrap alert
        flash(
            f"Brought a new stock " + stock + "! You have" +
            str(ownStock.unit) + " units of this stock remain", "success")
        db.session.add(ownStock)
      else:
        if action == "buy":
          ownStock.unit += int(quantity)
          ownStock.total_purchase_price += int(quantity) * float(
              checkout_form.data['current_market_price'])
          flash(
              f"Brought " + stock + "! You have " + str(ownStock.unit) +
              " units of this stock remain", "success")
        else:
          ownStock.unit -= int(quantity)
          ownStock.total_purchase_price -= int(quantity) * float(
              checkout_form.data['current_market_price'])
          flash(
              "Sold " + stock + "! You have " + str(ownStock.unit) +
              " units of this stock remain", "success")
          if ownStock.unit == 0:
            db.session.delete(ownStock)

      db.session.commit()
      return redirect(url_for('user.home'))

    # the cancel button is clicked.
    elif checkout_form.cancel.data:
      return redirect(url_for('stock.search_page', code=stock_obj.code))

  # checkout_form.data is a dict containing all fields value, e.g. {'current_market_price': None, 'total_price': None, 'submit': False, 'csrf_token': None}
  #checkout_form.data['current_market_price'] = get_search_result(stock_obj.code)['price']
  print(checkout_form.data)

  return render_template('checkout.html',
                         title='checkout',
                         stock_obj=stock_obj,
                         action=action,
                         quantity=quantity,
                         checkout_form=checkout_form)
