from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, MonthField
from wtforms.validators import InputRequired, Length, Email
from ..form_validation import ExcludeChars


class PurchaseInfoForm(FlaskForm):
    firstname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 99, "First Name must be less than 100 characters."),
        ]
    )
    lastname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 99, "Last Name must be less than 100 characters."),
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
            Email(),
            Length(1, 99, "Email must be less than 100 characters."),
        ]
    )

    cardnumber = IntegerField(validators=[InputRequired()])
    expirydate = MonthField(validators=[InputRequired()])
    cvv = IntegerField(validators=[InputRequired()])

    submit = SubmitField(validators=[InputRequired()])
