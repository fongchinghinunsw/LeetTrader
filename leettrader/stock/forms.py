from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from leettrader.models import Stock


class SearchStockForm(FlaskForm):
    stock = StringField('Stock', validators=[DataRequired()])

    submit = SubmitField('Search')
