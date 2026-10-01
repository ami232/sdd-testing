"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        result = validate_email("user@example.com")
        assert result == True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        result = validate_email("user@gmail.com")
        assert result == True, "TODO: Implement this test"

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        result = validate_email("userexample.com")
        assert result == False, "TODO: Implement this test"

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        result = validate_email("user@")
        assert result == False

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        result = validate_email("user@example")
        assert result == False

    def test_invalid_email_empty(self):
        """Test empty email."""
        result = validate_email("")
        assert result == False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        result = validate_email("user@@example.com")
        assert result == False
