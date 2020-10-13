import requests
from run import app
from leettrader import db, bcrypt
from leettrader.models import User, Stock


def create_db():
    """ Create the tables and database. """
    with app.app_context():
        db.create_all()


def drop_db():
    """ Delete the tables and database. """
    with app.app_context():
        db.drop_all()


def add_stocks():
    """ Add all the NZ stocks to the database. """
    stocks = requests.get(
        'https://finnhub.io/api/v1/stock/symbol?exchange=NZ&token=bthb6v748v6v983blvg0'
    ).json()
    with app.app_context():
        for stock in stocks:
            db.session.add(
                Stock(name=stock['description'], code=stock['symbol']))

        password_hashed = bcrypt.generate_password_hash("passw0rd").decode(
            'utf-8')
        admin = User(username="Donald Trump",
                     email="trump@leettrader.com",
                     password=password_hashed,
                     balance=0)
        db.session.add(admin)

        db.session.commit()


drop_db()
create_db()
add_stocks()
