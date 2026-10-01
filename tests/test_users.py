"""Exercise 2: integration tests and fixtures with teardown."""

import pytest

from orderflow.users import Database, UserRepository


class TestUserRepositoryIntegration:
    """Integration tests for UserRepository against a real Database."""

    @pytest.fixture
    def database(self):
        """Provide a connected database, and close it again afterwards."""
        database = Database()
        database.connect()
        yield database
        database.disconnect()
        raise NotImplementedError("TODO: Implement this fixture")

    @pytest.fixture
    def user_repo(self, database):
        """Provide a UserRepository backed by the connected database."""
        
        # TODO: Create and return a UserRepository with the database fixture
        raise NotImplementedError("TODO: Implement this fixture")

    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and then reading back a user."""
        # TODO: Create a user with id="123", name="John Doe", email="john@example.com"
        # TODO: Assert user['id'] == "123"
        # TODO: Assert user['name'] == "John Doe"
        # TODO: Assert user['email'] == "john@example.com"
        # TODO: Assert 'created_at' is in user

        # TODO: Retrieve the user by id "123"
        # TODO: Assert the retrieved user is not None
        # TODO: Assert retrieved['id'] == "123"
        # TODO: Assert retrieved['name'] == "John Doe"
        assert False, "TODO: Implement this test"

    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating a user with an invalid email raises."""
        # TODO: Use pytest.raises(ValueError, match="Invalid email")
        # TODO: Try to create a user with email="invalid-email"
        assert False, "TODO: Implement this test"

    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that does not exist."""
        # TODO: Get the user with id="999"
        # TODO: Assert the result is None
        assert False, "TODO: Implement this test"

    def test_database_not_connected_raises_error(self):
        """Test that operations fail when the database is not connected."""
        # TODO: Create a Database instance and do NOT connect it
        # TODO: Create a UserRepository with this database
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to create a user
        assert False, "TODO: Implement this test"

    def test_get_on_disconnected_database_raises_error(self):
        """Test that reads fail too, not only writes."""
        # TODO: Create a UserRepository over an unconnected Database
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to read a user
        assert False, "TODO: Implement this test"
