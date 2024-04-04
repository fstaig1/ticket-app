from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from ..form_validation import ExcludeChars, validate_password


class RegisterForm(FlaskForm):
    passwordError = "Password must be between 8 and 30 characters in length."
    firstname = StringField(
        validators=[InputRequired(), ExcludeChars("*?!'^+%&/\()=}][{$#@<>£~|¬`¦@;:_")]
    )
    lastname = StringField(
        validators=[InputRequired(), ExcludeChars("*?!'^+%&/\()=}][{$#@<>£~|¬`¦@;:_")]
    )
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(
        validators=[
            InputRequired(),
            Length(min=8, max=30, message=passwordError),
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
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
