from wtforms.validators import ValidationError
import re


def validate_password(self, password):
    """regex compiler to ensure passwords use at least 1 digit, 1 uppercase letter, 1 lower case letter, and 1 special character.

    Args:
        password (str): password

    Raises:
        ValidationError
    """
    # i mean this looks disastrous doesnt it
    p = re.compile(r"(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])")

    if not p.match(str(self.password.data).strip()):
        raise ValidationError(
            "Invalid password, please use at least 1 digit, 1 uppercase letter, 1 lower case letter, and 1 special character."
        )


def validate_email(self, email):
    """regex compiler to ensure proper email formatting

    Args:
        email (str): email

    Raises:
        ValidationError
    """
    p = re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}")

    if not p.match(str(self.email.data).strip()):
        raise ValidationError("Invalid Email.")
