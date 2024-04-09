from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class CreateConcertForm(FlaskForm):
    """FlaskForm for creating Concerts on the venue page

    Fields: artistName, date, capacity, ticketPrice, submit.
    """
    artistName = StringField(
        validators=[
            InputRequired(),
            Length(1, 30, "Artist name must be between 1 and 30 characters in length."),
        ]
    )
    date = StringField(validators=[InputRequired()])
    capacity = IntegerField(validators=[InputRequired()])
    ticketPrice = IntegerField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])


class CreateVenueForm(FlaskForm):
    """FlaskForm for creating new Venue on the venue page

    Fields: name, location, capacity, submit.
    """
    name = StringField(
        validators=[
            InputRequired(),
            Length(1, 30, "Name must be between 1 and 30 characters in length."),
        ]
    )
    location = StringField(
        validators=[
            InputRequired(),
            Length(1, 30, "Location must be between 1 and 30 characters in length."),
        ]
    )
    capacity = IntegerField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
