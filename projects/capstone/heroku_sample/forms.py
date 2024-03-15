from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL


class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    release_date = DateTimeField(
        'release_date', validators=[DataRequired()],
        default=datetime.today()
    )

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    gender = StringField('gender', validators=[DataRequired()]
    )