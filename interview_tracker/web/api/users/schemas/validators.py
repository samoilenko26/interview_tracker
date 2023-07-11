import re

from interview_tracker.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
    MIN_LENGTH_EMAIL,
    MIN_LENGTH_USERNAME,
)


def validate_username(username: str) -> str:
    username = username.strip()
    # Check if the username contains only alphanumeric characters and underscores
    if not re.match("^[a-zA-Zа-яА-Я0-9 _-]+$", username):
        raise ValueError(
            "Invalid username. " "pattern: ^[a-zA-Zа-яА-Я0-9 _-]+$",
        )
    # Check if the username starts with a letter
    if not re.match("^[a-zA-Zа-яА-Я]", username):
        raise ValueError(
            "Invalid username. First symbol should be a letter. ",
        )

    # Check if the username is between 3 and 20 characters long
    if len(username) < MIN_LENGTH_USERNAME or len(username) > MAX_LENGTH_USERNAME:
        raise ValueError(
            f"Invalid username. "
            f"Length should be >= {MIN_LENGTH_USERNAME} and <= {MAX_LENGTH_USERNAME}",
        )

    return username


def validate_email(email: str) -> str:
    email = email.strip()
    # Check if the username contains only alphanumeric characters and underscores
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):  # noqa: W605
        raise ValueError(
            "Invalid email address. pattern: ^[\w\.-]+@[\w\.-]+\.\w+$",  # noqa: W605
        )

    if len(email) < MIN_LENGTH_EMAIL or len(email) > MAX_LENGTH_EMAIL:
        raise ValueError(
            "Invalid email address. "
            f"Length should be >= {MIN_LENGTH_EMAIL} and <= {MAX_LENGTH_EMAIL}",
        )

    return email
