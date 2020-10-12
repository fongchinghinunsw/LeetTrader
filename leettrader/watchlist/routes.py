from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from leettrader import db
from leettrader.models import User, Watchlist
from leettrader.stock.utils import get_search_result
from leettrader.watchlist.utils import add_stocks, remove_stocks, get_list
from flask_login import current_user, login_required

watchlist = Blueprint('watchlist', __name__)

# simple routing as resources, the first two did nothing except returning success , the thrid one return a json to the frontend

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
    
@watchlist.route('/get_watchlist', methods=['GET'])
@login_required
def get_watchlist():
    return jsonify(watchlist = get_list(current_user)), 200
