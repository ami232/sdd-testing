"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        # TODO: Call validate_email with "user@example.com"
        # TODO: Assert the result is True
        #arrange
        email = "user@example.com"
        #act
        result = validate_email(email)
        #assert
        assert result is True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        # TODO: Call validate_email with "user@mail.example.com"
        # TODO: Assert the result is True
        #arrange
        email = "user@mail.example.com"
        #act
        result = validate_email(email)
        #assert
        assert result is True

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        # TODO: Call validate_email with "userexample.com"
        # TODO: Assert the result is False
        #arrange
        email = "userexample.com"
        #act
        result = validate_email(email)
        #assert
        assert result is False

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        # TODO: Call validate_email with "user@"
        # TODO: Assert the result is False
        #arrange
        email = "user@"
        #act
        result = validate_email(email)
        #assert
        assert result is False

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        # TODO: Call validate_email with "user@example"
        # TODO: Assert the result is False
        #arrange
        email = "user@example"
        #act
        result = validate_email(email)
        #assert
        assert result is False

    def test_invalid_email_empty(self):
        """Test empty email."""
        # TODO: Call validate_email with ""
        # TODO: Assert the result is False
        #arrange
        email = ""
        #act
        result = validate_email(email)
        #assert
        assert result is False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        # TODO: Call validate_email with "user@@example.com"
        # TODO: Assert the result is False
        #arrange
        email = "user@@example.com"
        #act
        result = validate_email(email)
        #assert
        assert result is False
