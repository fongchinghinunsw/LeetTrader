from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from leettrader.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  login_manager.init_app(app)
  bcrypt.init_app(app)
  
  # run this to reinitialize the database
  with app.app_context():
    db.create_all()

  from leettrader.main.routes import main
  from leettrader.user.routes import user
  from leettrader.stock.routes import stock
  from leettrader.watchlist.routes import watchlist

  app.register_blueprint(main)
  app.register_blueprint(user)
  app.register_blueprint(stock)
  app.register_blueprint(watchlist)

  return app
