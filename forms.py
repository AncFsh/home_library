from flask_wtf import FlaskForm
from wtforms import StringField


class Book(FlaskForm):
    title=StringField('Title')
    author=StringField('Author')
    rented=StringField('Rented')