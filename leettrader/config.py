import os

class Config:
  SECRET_KEY = '7b0dff182c1a883a7c12855dcc6f411d'
  SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False