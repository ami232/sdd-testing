"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        email = validate_email("user@example.com")
        assert email is True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        email = validate_email("user@mail.example.com")
        assert email is True

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        email = validate_email("userexample.com")
        assert email is False

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        email = validate_email("user@")
        assert email is False

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        email = validate_email("user@example")
        assert email is False

    def test_invalid_email_empty(self):
        """Test empty email."""
        email = validate_email("")
        assert email is False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        email = validate_email("user@@example.com")
        assert email is False
