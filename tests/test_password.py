"""Exercise 6: build orderflow/password.py with TDD."""

import pytest

from orderflow.password import validate_password


def test_password_shorter_than_eight_characters_is_rejected():
    """RED first: start here, with the length rule and nothing else."""
    # TODO: Call validate_password with a short password, e.g. "Ab1!"
    # TODO: Assert "Password must be at least 8 characters long" is in the result
    result = validate_password("Ab1!")
    assert "Password must be at least 8 characters long" in result


# TODO: Add one test per remaining rule from the README, in order:
# TODO:   uppercase, lowercase, digit, special character
# TODO: Then add a test that a fully valid password returns an empty list.
# TODO: Finally, add a test that a password breaking several rules at once
# TODO: reports every broken rule, not just the first.