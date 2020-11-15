from leettrader.models import User
from leettrader import bcrypt


def test_new_user(new_user):
  """
  GIVEN a User model
  WHEN a new User is created
  THEN check the email, hashed password, and user type are defined correctly
  """
  assert new_user.email == 'Oliver@leettrader.com'
  assert new_user.password != 'iloveu'
  assert not new_user.user_type == 1
