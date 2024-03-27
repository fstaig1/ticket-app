from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Length


class InputCheck():
    def __call__(self, form, field):
        for char in field.data:
            if char not in self.characters:
                raise ValidationError(self.message)

    def __init__(self, characters, message):
        self.characters = characters
        self.message = message


class ConcertForm(FlaskForm):
    artistName = StringField(validators=[InputRequired(), Length(1, 99, "Artist name must be less than 100 characters.")])
    ticketPrice = StringField(validators=[InputRequired(), InputCheck("1234567890", "Please only enter numbers for ticket price.")])
    date = StringField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
