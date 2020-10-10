from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from leettrader.models import User

# forms for login and regsiter account
class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

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
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  
  submit = SubmitField('Log in')


