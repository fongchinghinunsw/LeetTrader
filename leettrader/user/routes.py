"""
  Routing of Account Mangement, Simul-Buy and Sell
"""
import os
import operator
import secrets
from flask import render_template, url_for, flash, redirect, Blueprint, jsonify, request

from leettrader.user.forms import (LoginForm, RegisterForm, resetRequestForm,
resetPasswordForm, deleteRequestForm, accountUpdatedForm, OrderForm, CheckoutForm, ReminderForm)

from leettrader.user.utils import add_and_start_reminder
from leettrader.stock.utils import get_search_result
from leettrader.models import User, Stock, OwnStock, Reminder, UserType
from leettrader import db, bcrypt, mail
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

from leettrader.user.send_emails import send_confirmation_email, send_reset_password_email, send_delete_account_email

user = Blueprint('users', __name__)

# ugly global variable for now
new_username = None
new_email = None
new_password = None


@user.route("/home")
@login_required
def home():
  ''' Home Page '''
  return render_template('home.html')
  
@user.route("/admin")
@login_required
def admin():
  pass

@user.route("/register", methods=['GET', 'POST'])
def register():
  ''' Register Page '''
  if current_user.is_authenticated:
    return redirect(url_for('users.home'))

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
    return redirect(url_for('users.login'))
  return render_template('register.html', title='register', form=rform)

@user.route("/confirm/<token>", methods=['GET', 'POST'])
def confirm(token):
  # check if the token is valid
  res = User.verify_confirmation_token(token)
  if res is False:
    flash('The token has expired !', 'warning')
    return redirect(url_for('users.register'))
  else:
    # if the user has already existed, the user wants to click it twice
    # redirect to the home page
    user = User.query.filter_by(email=new_email).first()
    if user:
      flash('The account has already been activated, Please login', 'success')
      return redirect(url_for('users.login'))

    # Push changes to database, go to Login page
    new_user = User(user_type = "NORMAL",
                username=new_username,
                email=new_email,
                password=new_password)

    
    # the first time when a new user clicked
    db.session.add(new_user)
    db.session.commit()
    flash('Account created successfully, please login', 'success')
    return redirect(url_for('users.login'))

@user.route("/login", methods=['GET', 'POST'])
def login():

  if current_user.is_authenticated:
    return redirect(url_for('users.home'))

  login_form = LoginForm()
  # When click login, read user inputs 
  if login_form.validate_on_submit():
    user = User.query.filter_by(email=login_form.email.data).first()

    # If both Email & Password are correct, go to Home Page
    if user and bcrypt.check_password_hash(user.password,
                                           login_form.password.data):                                     
      login_user(user, remember=login_form.remember.data)
      if user.is_admin():
        return redirect(url_for('users.admin', userID=user.id))
      else: 
        return redirect(url_for('users.home', userID=user.id))

    # Show Error message otherwise
    elif not user:
      flash('This email has not been registered yet', 'danger')
    else:
      flash('Wrong password, please try again', 'danger')

  # Fail to login, stay in login page
  return render_template('login.html', title='login', loginForm=login_form)

# save the user chosen icon to the local
def save_icon_pic(icon_file):
   
  # get the random hex number
  rand_hex = secrets.token_hex(8)
  # get the icon file suffix
  _, file_suffix = os.path.splitext(icon_file.filename)
  # get the icon name after hex
  icon_name = rand_hex + file_suffix
  # get the leettrader folder
  parent_dir = os.path.dirname(user.root_path)

   # remove the previous icon pic to save space
  prev_icon_path = os.path.join(parent_dir, 'static', 'account_icons', current_user.icon)
  if os.path.exists(prev_icon_path) and os.path.basename(prev_icon_path) != 'trump.jpg':
    os.remove(prev_icon_path)

  # get the whole icon file path
  icon_path = os.path.join(parent_dir, 'static', 'account_icons', icon_name)
  # save the file into the path we created
  icon_file.save(icon_path)
  return icon_name

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account_profile():
  update_form = accountUpdatedForm()
  update_form.username.data = current_user.username
  update_form.email.data = current_user.email
  user_icon = url_for('static', filename='account_icons/' + current_user.icon)
  if request.method == 'GET':
    return render_template('account_profile.html', title='User Account', icon=user_icon, update_form = update_form)
  
  if update_form.validate_on_submit():
    
    if update_form.icon.data:
      profile_icon_name = save_icon_pic(update_form.icon.data)
      current_user.icon = profile_icon_name

    current_user.username = update_form.username.data
    current_user.email = update_form.email.data
    db.session.commit()
    flash('Your account has been updated !', 'success')
    return redirect(url_for('users.account_profile'))
  

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
  # if form.validate_on_submit():
    # user = User.query.filter_by(email=form.email.data).first()
    # send_reset_password_email(user)
    # flash('An email has been sent to reset your password', 'info')
  #   return jsonify({'user-email': user.email})
  return render_template('reset_request.html', title='reset password', form=form)

@user.route("/process", methods=['POST'])
# process the json data
def process():
  userEmail = request.form['email']
  if not userEmail:
    return jsonify({'error': 'Please enter your email'})

  user = User.query.filter_by(email=userEmail).first()
   # if the user entered invalid email
  if not user:
    return jsonify({'error': 'Invalid email, please try again'})

  print("Email sending now... ", userEmail)
  # if the user entered valid email
  send_reset_password_email(user)
  
  return jsonify({'userEmail': userEmail})


@user.route("/resetPassword/<token>", methods=['GET', 'POST'])
# reset their password when the token is active
def reset_password_token(token):
  # if current_user.is_authenticated:
  #   return redirect(url_for('user.home'))
  # check if the token is valid
  user = User.verify_reset_password_token(token)
  if user is None:
    flash('The token has expired !', 'warning')
    return redirect(url_for('users.reset_request'))
  else:
    form = resetPasswordForm()
    if form.validate_on_submit():
      # Hash password & Read User Input
      password_hashed = bcrypt.generate_password_hash(
          form.password.data).decode('utf-8')
      user.password = password_hashed
      db.session.commit()
      flash('Account has been reset, please login !', 'success')
      return redirect(url_for('users.login'))
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
    # print(user)

    if bcrypt.check_password_hash(current_user.password, form.password.data):
      curr_user = User.query.filter_by(email=form.email.data).first()
      send_delete_account_email(curr_user)
      flash('An email has been sent to cancel your account', 'info')
      logout_user()
      return redirect(url_for('users.login'))
    else:
      flash('Wrong password, please try again', 'danger')

  return render_template('delete_request.html', title='Delete your account', delete_form=form)


@user.route("/deleteAcount/<token>", methods=['GET', 'POST'])
# reset their password when the token is active
def delete_account_token(token):
  # check if the token is valid
  user = User.verify_delete_account_token(token)
  if user is None:
    flash('The token has expired !', 'warning')
    return redirect(url_for('users.deleteRequest'))
  else:
    # do the deletion if the token is valid
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted successfully', 'success')
    return redirect(url_for('user.login'))


@user.route("/order/<string:action>/<string:stock>", methods=['GET', 'POST'])
@login_required
def order(stock, action):
  ''' Order Page '''
  order_form = OrderForm()
  
  if order_form.validate_on_submit():
    quantity = order_form.quantity.data
    transaction_type = order_form.transaction_type.data
    stock_id = Stock.query.filter_by(code=stock).first().id
    print(stock_id)

    if action == "buy":
      print("You are buying a stock")
      return redirect(
          url_for('users.checkout',
                  action=action,
                  stock=stock,
                  quantity=quantity,
                  transaction_type=transaction_type))

    elif action == "sell":
      ownStock = OwnStock.query.filter_by(user_id=current_user.get_id(),
                                          stock_id=stock_id).first()
      print("You don't own any this stock")
      if ownStock is not None and ownStock.unit >= quantity:
        print("Currently, you own", ownStock.unit, "units of stock")
        return redirect(
            url_for('users.checkout',
                    action=action,
                    stock=stock,
                    quantity=quantity,
                    transaction_type=transaction_type))
      else:
        flash('You do not have enough amount of this stock to sell', "danger")

  return render_template('order.html',
                         title='order',
                         stock=stock,
                         action=action,
                         order_form=order_form)


@user.route("/checkout/<string:action>/<string:stock>",
            methods=['GET', 'POST'])
@login_required
def checkout(stock, action):
  quantity = request.args.get('quantity')
  transaction_type = request.args.get('transaction_type')

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
      return redirect(url_for('users.home'))

    # the cancel button is clicked.
    elif checkout_form.cancel.data:
      return redirect(url_for('stocks.search_page', code=stock_obj.code))

  # checkout_form.data is a dict containing all fields value, e.g. {'current_market_price': None, 'total_price': None, 'submit': False, 'csrf_token': None}
  #checkout_form.data['current_market_price'] = get_search_result(stock_obj.code)['price']
  print(checkout_form.data)

  return render_template('checkout.html',
                         title='checkout',
                         stock_obj=stock_obj,
                         action=action,
                         quantity=quantity,
                         checkout_form=checkout_form)

@user.route("/add_reminder", methods=['GET', 'POST'])
@login_required
def add_reminder():
  code = request.args.get('stock')
  reminder_form = ReminderForm()

  if reminder_form.validate_on_submit():
    if reminder_form.cancel.data:
      return redirect(url_for('stocks.search_page', code=code))

    # the user must enter the alert price.
    if reminder_form.alert_price.data:
      stock_obj = Stock.query.filter_by(code=code).first()
      reminder = Reminder(user_id=current_user.get_id(), stock_id=stock_obj.get_id(), orig_price=get_search_result(stock_obj.code)['price'], target_price=reminder_form.alert_price.data)
      add_and_start_reminder(reminder, current_user.username)
      return redirect(url_for('stocks.search_page', code=code))
      
    flash("Please enter a price.", "warning")

  return render_template('add_reminder.html', code=code, reminder_form=reminder_form)

class ReminderListItem:
  def __init__(self, stock_id, stock, reminder):
    self.stock_id = stock_id
    self.stock = stock
    self.reminder_list = [reminder]


@user.route("/view_reminder")
@login_required
def view_reminder():
  reminders = Reminder.get_reminders_by_user_id(current_user.id)

  reminder_items_dict = {}
  for reminder in reminders:
    if reminder.get_stock_id() not in reminder_items_dict:
      stock = Stock.query.filter_by(id=reminder.get_stock_id()).first()
      reminder_items_dict[reminder.get_stock_id()] = ReminderListItem(stock.id, stock, reminder)
    else:
      reminder_items_dict[reminder.get_stock_id()].reminder_list.append(reminder)

  reminder_items_list = list(reminder_items_dict.values())
  reminder_items_list.sort(key=operator.attrgetter('stock_id'))
      

  return render_template('reminder.html', reminder_items_list=reminder_items_list)


@user.route("/delete_reminder")
@login_required
def delete_reminder():
  reminder_id = request.args.get('reminder_id')
  db.session.query(Reminder).filter(Reminder.id==reminder_id).delete()
  db.session.commit()

  return redirect(url_for('users.view_reminder'))

  
  
