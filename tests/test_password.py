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
    
    result = validate_password('Ab1!')

    assert result == ['Password must be at least 8 characters long']

def test_password_requires_uppercase():
    """RED first: start here, with the length rule and nothing else."""
    
    result = validate_password('abcdef1!')

    assert result == ['Password must contain an uppercase letter']

def test_password_requires_lowercase():
    """RED first: start here, with the length rule and nothing else."""
    
    result = validate_password('ABCDEF1!')

    assert result == ['Password must contain a lowercase letter']

def test_password_requires_digit():
    """RED first: start here, with the length rule and nothing else."""
    
    result = validate_password('Abcdefg!')

    assert result == ['Password must contain a digit']

def test_password_requires_sepcial_character():
    """RED first: start here, with the length rule and nothing else."""
    
    result = validate_password('Abcdefg1')

    assert result == ['Password must contain a special character']



# TODO: Add one test per remaining rule from the README, in order:
# TODO:   uppercase, lowercase, digit, special character
# TODO: Then add a test that a fully valid password returns an empty list.
# TODO: Finally, add a test that a password breaking several rules at once
# TODO: reports every broken rule, not just the first.
