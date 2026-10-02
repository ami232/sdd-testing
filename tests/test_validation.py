"""Exercise 1b: unit tests for input validation."""

from orderflow.validation import validate_email


class TestValidateEmail:
    """Unit tests for email validation."""

    def test_valid_email(self):
        """Test valid email format."""
        email = 'user@example.com'

        result = validate_email(email=email)

        assert result == True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        email = 'user@mail.example.com'

        result = validate_email(email=email)

        assert result == True

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        email = 'userexample.com'

        result = validate_email(email=email)

        assert result == False

    def test_invalid_email_no_domain(self):
        """Test invalid email without domain."""
        email = 'user@'

        result = validate_email(email=email)

        assert result == False  

    def test_invalid_email_no_tld(self):
        """Test invalid email without TLD."""
        email = 'user@example'

        result = validate_email(email=email)

        assert result == False  

    def test_invalid_email_empty(self):
        """Test empty email."""
        email = ''

        result = validate_email(email=email)

        assert result == False

    def test_invalid_email_multiple_at(self):
        """Test email with multiple @ symbols."""
        email = 'user@@example.com'

        result = validate_email(email=email)

        assert result == False  
