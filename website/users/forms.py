from flask_wtf import FlaskForm
import re
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError   # noqa: F401


def character_check(form, field):
    excluded_chars = "*?!'^+%&/\()=}][{$#@<>"  # noqa: W605
    # FIXME i get a failed escape character error sometimes
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


def validate_password(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])')  # i mean this looks disastrous doesnt it
    if not p.match(self.password.data):
        raise ValidationError("Invalid password, please use at least 1 digit, 1 uppercase letter, 1 lower case letter, and 1 special character.")


class RegisterForm(FlaskForm):
    passwordError = "Password must be between 8 and 30 characters in length."
    firstname = StringField(validators=[InputRequired(), character_check])
    lastname = StringField(validators=[InputRequired(), character_check])
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30, message=passwordError), validate_password])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo("password", message="Both password fields must be equal.")])
    submit = SubmitField(validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField(validators=[InputRequired()])
