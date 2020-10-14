"""
  Flask form for Search Page
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchStockForm(FlaskForm):
  stock = StringField('Stock', validators=[DataRequired()])
  submit = SubmitField('Search')
