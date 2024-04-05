from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Optional
from ..form_validation import ExcludeChars, validate_password


class AdminCreateUserForm(FlaskForm):
    """FlaskForm for creating new users on the admin page.

    Fields: firstname, lastname, email, password, confirm_password, role, venueid, submit.
    """

    passwordError = "Password must be between 8 and 30 characters in length."

    firstname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 99, "First Name must be less than 100 characters."),
        ]
    )
    lastname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
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
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(
                min=8,
                max=30,
                message="Password must be between 8 and 30 characters in length.",
            ),
            validate_password,
        ]
    )
    confirm_password = PasswordField(
        validators=[
            InputRequired(),
            EqualTo("password", message="Both password fields must be equal."),
        ]
    )
    role = SelectField(
        choices=[("user", "User"), ("admin", "Admin"), ("venue", "Venue")],
        validators=[InputRequired()],
    )
    venueId = IntegerField(validators=[Optional()])
    submit = SubmitField(validators=[InputRequired()])


class AdminCreateVenueForm(FlaskForm):
    """FlaskForm for creating new venues on the admin page.

    Fields: name, location, capacity, submit.
    """
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
