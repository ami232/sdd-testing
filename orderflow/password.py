"""
Password strength rules.

Exercise 6 builds this module with TDD, so it starts out unimplemented.
Write a failing test first (red), then the smallest change that passes it
(green), then tidy up (refactor). Repeat, one rule at a time.
"""

from typing import List

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.<>?/"


# Each rule pairs a check that must hold with the message reported when it does not.
RULES = [
    (lambda p: len(p) >= 8, "Password must be at least 8 characters long"),
    (lambda p: any(c.isupper() for c in p), "Password must contain an uppercase letter"),
    (lambda p: any(c.islower() for c in p), "Password must contain a lowercase letter"),
    (lambda p: any(c.isdigit() for c in p), "Password must contain a digit"),
    (
        lambda p: any(c in SPECIAL_CHARACTERS for c in p),
        "Password must contain a special character",
    ),
]


def validate_password(password: str) -> List[str]:
    """
    Check a password against the strength rules.

    Returns:
        A list of error messages, one per broken rule, in any order. An empty
        list means the password is valid.

    The rules and their exact messages are listed in the README.
    """
    return [message for check, message in RULES if not check(password)]
