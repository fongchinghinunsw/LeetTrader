from utils import init_db
from flask import url_for
from flask_login import login_manager, login_user
from leettrader.models import User
def test_login_page(test_client):
  # try get the login page
  response = test_client.get('/login')
  print(response.data)
  assert response.status_code == 200
  assert b"Email" in response.data
  assert b"Password" in response.data
  assert b"Log in" in response.data

def test_valid_login_logout(test_client, init_database):
  # try to log oliver in
  url = url_for('users.login')
  response = test_client.post(url,
                              data=dict(email='trump@leettrader.com', password='passw0rd'),
                              follow_redirects=True)
  user = User.query.filter_by(email='trump@leettrader.com').first()
  login_user(user)
  assert response.status_code == 200
  assert b'Log in' in response.data
  # # ty to log oliver out
  response = test_client.get('/logout', follow_redirects=True)
  assert response.status_code == 200
  assert b'Have you tried virtual trading?' in response.data
  init_db()

def test_invalid_login(test_client, init_database):

  response = test_client.post('/login',
                              data=dict(email='oliverGuoleetrader.com', password='passw0rd'),
                              follow_redirects=True)
  assert response.status_code == 200
  assert b"Invalid email address." in response.data
  assert b"Email" in response.data
  assert b"Password" in response.data
  assert b"Log in" in response.data


def test_valid_registration(test_client, init_database):
  # register user with valid information
  response = test_client.post('/register',
                              data=dict(username="valid username",
                                        email='valid@leettrader.com',
                                        password='passw0rd',
                                        confirm_password='passw0rd'),
                              follow_redirects=True)
  assert response.status_code == 200
  # assert b"Confirmation email has been sent, please check your emails" in response.data
  assert b"Email" in response.data
  assert b"Password" in response.data
  assert b"Sign Up" in response.data

def test_invalid_registration(test_client, init_database):
  # register user with invalid information
  response = test_client.post('/register',
                              data=dict(username="my",
                                        email='trump@leettrader.com',
                                        password='passw0rd',
                                        confirm_password='password'),
                              follow_redirects=True)
  assert response.status_code == 200
  assert b"the email has been registered. Please log in" in response.data
  assert b"Field must be equal to password." in response.data