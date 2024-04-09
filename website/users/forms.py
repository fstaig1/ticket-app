from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from ..form_validation import ExcludeChars, validate_password


class RegisterForm(FlaskForm):
    """FlaskForm for user registration.

    Fields: firstname, lastname, email, password, confirm_password, submit.
    """

    firstname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 30, "First Name must be between 1 and 30 characters."),
        ]
    )
    lastname = StringField(
        validators=[
            InputRequired(),
            ExcludeChars("*?!'^+%&/\\()=}][{$#@<>£~|¬`¦@;:_"),
            Length(1, 30, "Last Name must be between 1 and 30 characters."),
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
            Email(),
            Length(1, 30, "Email must be less than 30 characters."),
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
    submit = SubmitField(validators=[InputRequired()])


class LoginForm(FlaskForm):
    """FlaskForm for user logins.

    Fields: email, password, submit.
    """

    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
