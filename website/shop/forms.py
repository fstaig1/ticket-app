from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, MonthField
from wtforms.validators import InputRequired, Length, Regexp
from ..form_validation import validate_email


class PurchaseInfoForm(FlaskForm):
    firstname = StringField(
        validators=[
            InputRequired(),
            Regexp(
                "^[a-zA-Z',.\s-]+$",
                message="Invalid name, make sure you are not using any numbers or special characters outside of the following ' , . -",
            ),
            Length(1, 30, "First Name must be between 1 and 30 characters in length."),
        ]
    )
    lastname = StringField(
        validators=[
            InputRequired(),
            Regexp(
                "^[a-zA-Z',.\s-]+$",
                message="Invalid name, make sure you are not using any numbers or special characters outside of the following ' , . -",
            ),
            Length(1, 30, "Last Name must be between 1 and 30 characters in length."),
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
            validate_email,
            Length(1, 30, "Email must be between 1 and 30 characters in length."),
        ]
    )
    cardnumber = IntegerField(
        validators=[
            InputRequired(),
        ]
    )
    expirydate = MonthField(validators=[InputRequired()])
    cvv = IntegerField(validators=[InputRequired()])

    submit = SubmitField(validators=[InputRequired()])
