"""Exercise 6: build orderflow/password.py with TDD."""

from orderflow.password import validate_password


def test_password_shorter_than_eight_characters_is_rejected():
    assert "Password must be at least 8 characters long" in validate_password("Ab1!")


def test_password_without_uppercase_is_rejected():
    assert "Password must contain an uppercase letter" in validate_password("abcdefg1!")


def test_password_without_lowercase_is_rejected():
    assert "Password must contain a lowercase letter" in validate_password("ABCDEFG1!")


def test_password_without_digit_is_rejected():
    assert "Password must contain a digit" in validate_password("Abcdefgh!")


def test_password_without_special_character_is_rejected():
    assert "Password must contain a special character" in validate_password("Abcdefg1")


def test_valid_password_returns_no_errors():
    assert validate_password("Abcdef1!") == []


def test_password_breaking_several_rules_reports_all_of_them():
    errors = validate_password("abc")

    assert set(errors) == {
        "Password must be at least 8 characters long",
        "Password must contain an uppercase letter",
        "Password must contain a digit",
        "Password must contain a special character",
    }
