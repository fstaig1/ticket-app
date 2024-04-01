from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class ConcertForm(FlaskForm):
    artistName = StringField(
        validators=[
            InputRequired(),
            Length(1, 99, "Artist name must be less than 100 characters."),
        ]
    )
    ticketPrice = IntegerField(validators=[InputRequired()])
    date = StringField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
