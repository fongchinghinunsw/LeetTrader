""" Create test fixtures """

import os
import tempfile

import pytest
from leettrader import create_app
from leettrader import bcrypt, db
from run import app
from utils import init_db

from leettrader.models import User

# test for having a new user
@pytest.fixture(scope="module")
def new_user():
  mypassword_hashed = bcrypt.generate_password_hash("iloveu").decode('utf-8')
  new_user = User(user_type = "ADMIN",
            username="Oliver",
            email="Oliver@leettrader.com",
            password=mypassword_hashed)
  return new_user

@pytest.fixture(scope='module')
def test_client():
  """ This client fixture will be called by each individual test """
  # returns a low-level file handle and a random file name
  db_fd, app.config['DATABASE'] = tempfile.mkstemp()
  # disable error catching during request handling, so that you get
  # better error reports when performing test requests against the application.
  app.config['TESTING'] = True

  with app.test_client() as testing_client:
    with app.app_context():
      init_db()

    print("yield the client")
    yield testing_client

  os.close(db_fd)
  os.unlink(app.config['DATABASE'])

# create and initialise the db, drop all after testing
@pytest.fixture(scope='module')
def init_database(test_client):
  # # Create the database and the database table
  init_db()

  stephen_password_hashed = bcrypt.generate_password_hash("stephen").decode('utf-8')
  OliverGuo_password_hashed = bcrypt.generate_password_hash("oliverGuo").decode('utf-8')
  # Insert user data
  user1 = User(user_type = "NORMAL",
          username="stephen",
          email="stephen@leettrader.com",
          password=stephen_password_hashed)
  user2 = User(user_type = "NORMAL",
          username="OliverGuo",
          email="OliverGuo@leettrader.com",
          password=OliverGuo_password_hashed)
  db.session.add(user2)
 
  # Commit the changes for the users
  db.session.commit()
  # this is where the testing happens!
  yield db
  # reset the db
  init_db()