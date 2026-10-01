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


def test_password_without_special_character_is_rejected():
    """A password needs a character from the special-character set."""
    errors = validate_password("Abcdefg1")
    assert "Password must contain a special character" in errors


def test_valid_password_returns_no_errors():
    """A password that meets every rule is valid."""
    assert validate_password("Abcdef1!") == []


def test_password_breaking_several_rules_reports_all_of_them():
    """Every broken rule is reported, not only the first."""
    errors = validate_password("abc")
    assert set(errors) == {
        "Password must be at least 8 characters long",
        "Password must contain an uppercase letter",
        "Password must contain a digit",
        "Password must contain a special character",
    }
