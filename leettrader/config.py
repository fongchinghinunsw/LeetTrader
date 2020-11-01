import os
"""
  Config class: used for configuring the Flask app.
"""


class Config:
  SECRET_KEY = '7b0dff182c1a883a7c12855dcc6f411d'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  TESTING = False
  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USE_SSL = False
  # MAIL_DEBUG = True
  MAIL_USERNAME = 'leettrader2020@gmail.com'
  MAIL_PASSWORD = 'IronMan123@'
  MAIL_DEFAULT_SENDER = ('LeetTrader', 'noreplypls@gmail.com')
  # MAIL_MAX_EMAILS = None
  # MAIL_SUPPRESS_SEND = False
  # MAIL_ASCII_ATTACHMENTS = False

