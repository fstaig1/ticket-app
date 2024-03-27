from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import InputRequired


class ConcertForm(FlaskForm):
    artistName = StringField(validators=[InputRequired()])
    ticketPrice = IntegerField(validators=[InputRequired()])
    date = DateTimeField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
