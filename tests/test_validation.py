"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        assert validate_email("user@example.com") is True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        assert validate_email("user@mail.example.com") is True

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        assert validate_email("userexample.com") is False

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        assert validate_email("user@") is False

    def test_invalid_email_no_username(self):
        """Test invalid email without the part before the @."""
        assert validate_email("@example.com") is False

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        assert validate_email("user@example") is False

    def test_invalid_email_empty(self):
        """Test empty email."""
        assert validate_email("") is False

    def test_invalid_email_none(self):
        """Test that None is rejected rather than crashing."""
        assert validate_email(None) is False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        assert validate_email("user@@example.com") is False
