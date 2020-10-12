from flask import render_template, request, redirect, url_for, Blueprint
from leettrader import db
from leettrader.models import User, Watchlist
from leettrader.stock.utils import get_search_result
from leettrader.watchlist.utils import add_stocks, remove_stocks
from flask_login import current_user, login_required

watchlist = Blueprint('watchlist', __name__)

@watchlist.route('/add/<string:code>', methods=['POST'])
@login_required
def add_stock_to_watchlist(code):
    add_stocks(current_user, code)
    return {"msg": "Added"}, 200

@watchlist.route('/remove/<string:code>', methods=['POST'])
@login_required
def remove_stock_from_watchlist(code):
    remove_stocks(current_user, code)
    return {"msg": "Deleted"}, 200
