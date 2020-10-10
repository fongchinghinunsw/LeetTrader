from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from leettrader.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)

  # run this to reinitialize the database
  #with app.app_context():
  #  db.create_all()

  from leettrader.main.routes import main
  from leettrader.stock.routes import stock

  app.register_blueprint(main)
  app.register_blueprint(stock)

  return app