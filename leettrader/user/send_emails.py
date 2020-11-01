from leettrader import mail
from flask_mail import Message
from flask import url_for

# Use flask-mail to send the email
def send_confirmation_email(new_user):
  # get a new token and start timer !
  token = new_user.get_new_token()
  msg = Message('Confirmation for new account', sender='leettrader2020@gmail.com', recipients=[new_user.email])
  msg.body = f'''Dear {new_user.username}, to confirm your email and activate your new account, please click the link below:
{url_for('users.confirm', token=token, _external=True)}

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
{url_for('users.reset_password_token', token=token, _external=True)}

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
{url_for('users.delete_account_token', token=token, _external=True)}
Please be aware that all your account information and data will be deleted and cannot be retrieved.

If you did not make the request, please just ignore this email.

Cheers,
LeetTrader Team
  '''
  mail.send(msg)
