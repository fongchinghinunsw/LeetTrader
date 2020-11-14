"""
  WTFroms of:
    1. Register 
    2. Login
    3. Order
    4. Checkout
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange
from leettrader.models import User
from flask_login import current_user


# forms for login and regsiter account
class RegisterForm(FlaskForm):
  ''' Register Form '''
  username = StringField(
      'Username',
      validators=[
          DataRequired(),
          Length(message="Username must be between 2 and 20 characters long",
                 min=2,
                 max=20)
      ])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField(
      'Password',
      validators=[
          DataRequired(),
          Length(message="Password must be between 6 and 30 characters long",
                 min=6,
                 max=30)
      ])
  confirm_password = PasswordField(
      'Confirm Password', validators=[DataRequired(),
                                      EqualTo('password')])

  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('the username has been taken')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('the email has been registered. Please log in')


class LoginForm(FlaskForm):
  ''' Login Form '''
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Log in')


class resetRequestForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Send Request')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None:
      raise ValidationError('This email has not been registered yet')

class resetPasswordForm(FlaskForm):
  password = PasswordField(
      'Password',
      validators=[
          DataRequired(),
          Length(message="Password must be between 6 and 30 characters long",
                 min=6,
                 max=30)
      ])
  confirm_password = PasswordField(
      'Confirm Password', validators=[DataRequired(),
                                      EqualTo('password')])

  submit = SubmitField('Reset Password')

class deleteRequestForm(FlaskForm):
  ''' delete account request Form '''
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Confirm and Send Request')




class accountUpdatedForm(FlaskForm):
  ''' direct change username and password Form '''
  username = StringField(
      'Username',
      validators=[
          DataRequired(),
          Length(message="Username must be between 2 and 20 characters long",
                 min=2,
                 max=20)
      ])

  email = StringField('Email', validators=[DataRequired(), Email()])
  icon = FileField('Change Your Icon ', validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
  submit = SubmitField('Update')

  def validate_username(self, username):
    if username.data != current_user.username:
  
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('The username has been taken')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('The email has been registered')



class OrderForm(FlaskForm):
  ''' Stock Order Form '''
  quantity = IntegerField('Quantity',
                          validators=[
                              DataRequired(message="please enter an integer"),
                              NumberRange(
                                  message="Quantity must be at least 1", min=1)
                          ])
  transaction_types = ['Current Market Price']
  transaction_type = SelectField('Transaction Type', choices=transaction_types)
  submit = SubmitField('Proceed')


class CheckoutForm(FlaskForm):
  ''' Stock Order Checkout Form '''
  current_market_price = StringField('current_market_price',
                                     render_kw={'readonly': True})
  total_price = StringField('total_price', render_kw={'readonly': True})
  submit = SubmitField('Checkout')
  cancel = SubmitField('Cancel')


class ReminderForm(FlaskForm):
  ''' Reminder Form '''
  alert_price = StringField('Alert Price')
  submit = SubmitField('Confirm')
  cancel = SubmitField('Cancel')
