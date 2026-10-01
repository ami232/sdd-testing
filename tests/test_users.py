"""Exercise 2: integration tests and fixtures with teardown."""

import pytest

from orderflow.users import Database, UserRepository


class TestUserRepositoryIntegration:
    """Integration tests for UserRepository against a real Database."""

    @pytest.fixture
    def database(self):
        """Provide a connected database, and close it again afterwards."""
        # TODO: Create a Database instance
        # TODO: Call connect() on the database
        # TODO: Use yield to hand the database to the test
        # TODO: After the yield, call disconnect() on the database
        db = Database()
        db.connect()
        yield db
        db.disconnect()

    @pytest.fixture
    def user_repo(self, database):
        """Provide a UserRepository backed by the connected database."""
        # TODO: Create and return a UserRepository with the database fixture
        return UserRepository(database)

    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and then reading back a user."""
        # TODO: Create a user with id="123", name="John Doe", email="john@example.com"
        # TODO: Assert user['id'] == "123"
        # TODO: Assert user['name'] == "John Doe"
        # TODO: Assert user['email'] == "john@example.com"
        # TODO: Assert 'created_at' is in user
        user = user_repo.create_user(
            user_id="123",
            name="John Doe",
            email="john@example.com"
        )

        assert user["id"] == "123"
        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
        assert "created_at" in user

        # TODO: Retrieve the user by id "123"
        # TODO: Assert the retrieved user is not None
        # TODO: Assert retrieved['id'] == "123"
        # TODO: Assert retrieved['name'] == "John Doe"
        retrieved = user_repo.get_user("123")

        assert retrieved is not None
        assert retrieved["id"] == "123"
        assert retrieved["name"] == "John Doe"

    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating a user with an invalid email raises."""
        # TODO: Use pytest.raises(ValueError, match="Invalid email")
        # TODO: Try to create a user with email="invalid-email"
        with pytest.raises(ValueError, match="Invalid email"):
            user_repo.create_user(
                user_id="123",
                name="John Doe",
                email="invalid-email"
            )

    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that does not exist."""
        # TODO: Get the user with id="999"
        # TODO: Assert the result is None
        result = user_repo.get_user("999")
        assert result is None

    def test_database_not_connected_raises_error(self):
        """Test that operations fail when the database is not connected."""
        # TODO: Create a Database instance and do NOT connect it
        # TODO: Create a UserRepository with this database
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to create a user
        db = Database()
        user_repo = UserRepository(db)

        with pytest.raises(ConnectionError, match="not connected"):
            user_repo.create_user(
                user_id="123",
                name="John Doe",
                email="john@example.com"
            )

    def test_get_on_disconnected_database_raises_error(self):
        """Test that reads fail too, not only writes."""
        # TODO: Create a UserRepository over an unconnected Database
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to read a user
        db = Database()
        user_repo = UserRepository(db)

        with pytest.raises(ConnectionError, match="not connected"):
            user_repo.get_user("123")