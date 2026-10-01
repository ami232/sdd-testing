"""
Password strength rules.

Exercise 6 builds this module with TDD, so it starts out unimplemented.
Write a failing test first (red), then the smallest change that passes it
(green), then tidy up (refactor). Repeat, one rule at a time.
"""

from typing import List

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def validate_password(password: str) -> List[str]:
    """
    Check a password against the strength rules.

    Returns:
        A list of error messages, one per broken rule, in any order. An empty
        list means the password is valid.

    The rules and their exact messages are listed in the README.
    """
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain an uppercase letter")
    if not any(c.islower() for c in password):
        errors.append("Password must contain a lowercase letter")
    return errors
