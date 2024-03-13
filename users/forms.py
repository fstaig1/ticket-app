from flask_wtf import FlaskForm
import re
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

def character_check(form, field):    
    excluded_chars = "*?!'^+%&/\()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")
            
def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])')
        if not p.match(self.password.data):
            raise ValidationError("Invalid password, please use at least 1 digit, 1 uppercase letter, 1 lower case letter, and 1 special character.")

class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), character_check])
    lastname = StringField(validators=[InputRequired(), character_check])
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=30, message="Password must be between 8 and 30 characters in length."), validate_password])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo("password", message="Both password fields must be equal.")])
    submit = SubmitField(validators=[InputRequired()])
    
