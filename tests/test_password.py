"""
Exercise 6: build orderflow/password.py with TDD.

This file is almost empty on purpose. Unlike every other exercise here, the
production code does not exist yet, so you write the test first and let the
failing test tell you what to implement next.

The cycle, one rule at a time:

  1. RED      Write one test for one rule. Run it. It must fail, and it must
              fail for the reason you expect.
  2. GREEN    Write the smallest change to orderflow/password.py that makes
              it pass. Do not implement rules you have no test for yet.
  3. REFACTOR Tidy up the implementation with the suite green.

The rules and their exact error messages are in the README. Work down that
list in order, and commit after each green step so your history shows the
cycle.
"""

import pytest

from orderflow.password import validate_password


def test_password_shorter_than_eight_characters_is_rejected():
    """RED first: start here, with the length rule and nothing else."""
    errors = validate_password("Ab1!")
    assert "Password must be at least 8 characters long" in errors


def test_password_without_uppercase_letter_is_rejected():
    """A long enough password still needs an uppercase letter."""
    errors = validate_password("abcdef1!")
    assert "Password must contain an uppercase letter" in errors


def test_password_without_lowercase_letter_is_rejected():
    """A password needs a lowercase letter."""
    errors = validate_password("ABCDEF1!")
    assert "Password must contain a lowercase letter" in errors


def test_password_without_digit_is_rejected():
    """A password needs a digit."""
    errors = validate_password("Abcdefg!")
    assert "Password must contain a digit" in errors
