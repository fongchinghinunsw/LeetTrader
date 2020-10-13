from flask import render_template, url_for, flash, redirect, Blueprint
from leettrader.user.forms import LoginForm, RegisterForm, OrderForm, CheckoutForm
from leettrader.models import User, Stock, OwnStock
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

#Order stocks
@user.route("/order/<string:action>/<string:stock>", methods=['GET', 'POST'])
@login_required
def order(stock, action):
  print("Reached")
  order_form = OrderForm()
  if order_form.validate_on_submit():
    quantity = order_form.quantity.data

    
    print(stock)
    stock_id = Stock.query.filter_by(code=stock).first().id
    print(stock_id)
    
    if action == "buy":
      return redirect(url_for('user.checkout', action=action, stock=stock, quantity=quantity))

    elif action == "sell":
      ownStock = OwnStock.query.filter_by(user_id = current_user.get_id(), stock_id=stock_id).first()
      print("You don't own any this stock")
      if ownStock is not None and ownStock.unit >= quantity:
        print("Currently, you own", ownStock.unit, "units of stock")
        return redirect(url_for('user.checkout', action=action, stock=stock, quantity=quantity))
      else:
        flash('You do not have enough amount of this stock to sell')
        

  
  return render_template('order.html', title='order', stock=stock, action=action, order_form=order_form)

@user.route("/checkout/<string:action>/<string:stock>/<quantity>", methods=['GET', 'POST'])
@login_required
def checkout(stock, action, quantity):
  stock_obj = Stock.query.filter_by(code=stock).first()
  stock_id = stock_obj.id;

  checkout_form = CheckoutForm()
  if checkout_form.validate_on_submit():
    ownStock = OwnStock.query.filter_by(user_id = current_user.get_id(), stock_id=stock_id).first()
    if ownStock is None:
      # only true if the action is buy.
      print("Brought a new stock! You have", quantity, "units of this stock remain")
      ownStock = OwnStock(user_id=current_user.get_id(), stock_id=stock_id, unit=quantity, total_purchase_price=quantity)
      db.session.add(ownStock)
    else:
      if action == "buy":
        ownStock.unit += int(quantity)
        print("Brought! You have", quantity, "units of this stock remain")
      else:
        ownStock.unit -= int(quantity)
        print("Sold! You have", quantity, "units of this stock remain")
        if ownStock.unit == 0:
          db.session.delete(ownStock)

    db.session.commit()
    return render_template('home.html')
    
  
  
  return render_template('checkout.html', title='checkout', stock_obj=stock_obj, action=action, quantity=quantity, checkout_form=checkout_form)