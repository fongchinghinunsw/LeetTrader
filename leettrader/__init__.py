from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
main = Blueprint('main', __name__)

app.config['SECRET_KEY'] = '7b0dff182c1a883a7c12855dcc6f411d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # construct relative path from the current file
app.register_blueprint(main)

# add functionalities to our flask application
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# prevent circular import
from leettrader.main import routes
