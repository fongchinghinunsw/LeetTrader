"""
  Main() to initialize databse and run flask app.
"""
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_appbuilder.api import expose

from leettrader.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
  ''' Create a flask webapp with an initialized database '''
  app = Flask(__name__)
  app.config.from_object(Config)

  # Admin page config
  from leettrader.models import User, TransactionRecord, Stock
  from leettrader.ownedList.reset import reset_account
  class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
      users = db.session.query(User).count()
      transactions = db.session.query(TransactionRecord).count()
      stocks = db.session.query(Stock).count()
      return self.render('admin/index.html',
                         users=users,
                         transactions=transactions,
                         stocks=stocks)

  class UserView(ModelView):
    can_edit = False
    can_create = False
    def delete_model(self, user):
      reset_account(user)
      self.session.delete(user)
      self.session.commit()
      return True
    

  app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
  admin = Admin(app,
                name='Admin',
                index_view=AdminView(),
                template_mode='bootstrap3')
  admin.add_view(UserView(User, db.session))

  db.init_app(app)
  login_manager.init_app(app)
  bcrypt.init_app(app)
  mail.init_app(app)

  # Re-initialize database
  with app.app_context():
    db.create_all()

  from leettrader.main.routes import main
  from leettrader.user.routes import user
  from leettrader.stock.routes import stock
  from leettrader.watchlist.routes import watchlist
  from leettrader.ownedList.routes import ownedList
  from leettrader.tutorial.chatbot import chatbot
  from leettrader.tutorial.routes import tutorial

  app.register_blueprint(main)
  app.register_blueprint(user)
  app.register_blueprint(stock)
  app.register_blueprint(watchlist)
  app.register_blueprint(ownedList)
  app.register_blueprint(chatbot)
  app.register_blueprint(tutorial)

  return app
