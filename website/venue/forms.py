from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class CreateConcertForm(FlaskForm):
    artistName = StringField(
        validators=[
            InputRequired(),
            Length(1, 99, "Artist name must be less than 100 characters."),
        ]
    )
    date = StringField(validators=[InputRequired()])
    capacity = IntegerField(validators=[InputRequired()])
    ticketPrice = IntegerField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])


class CreateVenueForm(FlaskForm):
    name = StringField(
        validators=[
            InputRequired(),
            Length(1, 99, "Name must be less than 100 characters."),
        ]
    )
    location = StringField(
        validators=[
            InputRequired(),
            Length(1, 99, "Location must be less than 100 characters."),
        ]
    )
    capacity = IntegerField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
