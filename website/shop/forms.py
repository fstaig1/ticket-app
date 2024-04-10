from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, MonthField
from wtforms.validators import InputRequired, Length, NumberRange
from ..form_validation import ExcludeChars, validate_email


class PurchaseInfoForm(FlaskForm):
    firstname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 30, "First Name must be between 1 and 30 characters in length."),
        ]
    )
    lastname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
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
            NumberRange(
                1000000000000000,
                9999999999999999,
                "Please enter a valid 16 digit card number.",
            ),
        ]
    )
    expirydate = MonthField(validators=[InputRequired()])
    cvv = IntegerField(validators=[InputRequired()])

    submit = SubmitField(validators=[InputRequired()])
