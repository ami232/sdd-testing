"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        # TODO: Call validate_email with "user@example.com"
        # TODO: Assert the result is True
        assert(validate_email("user@example.com") == True)

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        # TODO: Call validate_email with "user@mail.example.com"
        # TODO: Assert the result is True
        assert(validate_email("user@mail.example.com") == True)

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        # TODO: Call validate_email with "userexample.com"
        # TODO: Assert the result is False
        assert(validate_email("userexample.com") == False)

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        # TODO: Call validate_email with "user@"
        # TODO: Assert the result is False
        assert(validate_email("user@") == False)

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        # TODO: Call validate_email with "user@example"
        # TODO: Assert the result is False
        assert(validate_email("user@example") == False)

    def test_invalid_email_empty(self):
        """Test empty email."""
        # TODO: Call validate_email with ""
        # TODO: Assert the result is False
        assert(validate_email("") == False)
        

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        # TODO: Call validate_email with "user@@example.com"
        # TODO: Assert the result is False
        assert(validate_email("user@@example.com") == False)
