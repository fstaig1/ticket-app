from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Optional, Regexp
from ..form_validation import validate_password, validate_email


class AdminCreateUserForm(FlaskForm):
    """FlaskForm for creating new users on the admin page.

    Fields: firstname, lastname, email, password, confirm_password, role, venueid, submit.
    """

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
                message="Invalid name, make sure you are not using any numbers or special characters outside of the following ',. -",
            ),
            Length(1, 30, "Last Name must be between 1 and 30 characters in length."),
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
            validate_email,
            Length(1, 60, "Email must be between 1 and 60 characters in length."),
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

    Fields: name, location, capacity, managerId, submit.
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
    managerId = IntegerField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
