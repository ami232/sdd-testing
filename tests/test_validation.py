"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        # TODO: Call validate_email with "user@example.com"
        email = "user@example.com"
        result = validate_email(email)

        # TODO: Assert the result is True
        assert result is True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        # TODO: Call validate_email with "user@mail.example.com"
        email = "user@mail.example.com"
        result = validate_email(email)
        # TODO: Assert the result is True
        assert result is True

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        # TODO: Call validate_email with "userexample.com"
        email = "userexample.com"
        result = validate_email(email)
        # TODO: Assert the result is False
        assert result is False

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        # TODO: Call validate_email with "user@"
        email = "user@"
        result = validate_email(email)
        # TODO: Assert the result is False
        assert result is False
        

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        # TODO: Call validate_email with "user@example"
        email = "user@example"
        result = validate_email(email)
        # TODO: Assert the result is False
        assert result is False

    def test_invalid_email_empty(self):
        """Test empty email."""
        # TODO: Call validate_email with ""
        email = ""
        result = validate_email(email)
        # TODO: Assert the result is False
        assert result is False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        # TODO: Call validate_email with "user@@example.com"
        email = "user@@example.com"
        result = validate_email(email)
        # TODO: Assert the result is False
        assert result is False
