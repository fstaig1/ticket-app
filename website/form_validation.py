from wtforms.validators import ValidationError
import re


class IncludeChars():
    def __call__(self, form, field):
        for char in field.data:
            if char not in self.characters:
                raise ValidationError(self.message)

    def __init__(self, characters, message):
        self.characters = characters
        self.message = message


class ExcludeChars():
    def __call__(self, form, field):
        for char in field.data:
            if char in self.characters:
                raise ValidationError(f"Character {char} is not allowed.")

    def __init__(self, characters):
        self.characters = characters


def validate_password(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])')  # i mean this looks disastrous doesnt it
    if not p.match(self.password.data):
        raise ValidationError("Invalid password, please use at least 1 digit, 1 uppercase letter, 1 lower case letter, and 1 special character.")
