"""Exercise 2: integration tests and fixtures with teardown."""

from unicodedata import name

import pytest

from orderflow.users import Database, UserRepository


class TestUserRepositoryIntegration:
    """Integration tests for UserRepository against a real Database."""

    @pytest.fixture
    def database(self):
        """Provide a connected database, and close it again afterwards."""
        # TODO: Create a Database instance
        db = Database()
        # TODO: Call connect() on the database
        db.connect()
        # TODO: Use yield to hand the database to the test
        yield db
        # TODO: After the yield, call disconnect() on the database
        db.disconnect()                                                  

    @pytest.fixture
    def user_repo(self, database):
        """Provide a UserRepository backed by the connected database."""
        # TODO: Create and return a UserRepository with the database fixture
        return UserRepository(database) 

    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and then reading back a user."""
        # TODO: Create a user with id="123", name="John Doe", email="john@example.com"
        id = "123"
        name = "John Doe"
        email = "john@example.com"
        user_repo.create_user(id, name, email)
        # TODO: Assert user['id'] == "123"
        assert user_repo.get_user(id)['id'] == "123"   
        # TODO: Assert user['name'] == "John Doe"
        assert user_repo.get_user(id)['name'] == name

        # TODO: Assert user['email'] == "john@example.com"
        assert user_repo.get_user(id)['email'] == "john@example.com"
        # TODO: Assert 'created_at' is in user
        assert 'created_at' in user_repo.get_user(id)
        # TODO: Retrieve the user by id "123"
        retrieved = user_repo.get_user(id)
        # TODO: Assert the retrieved user is not None
        assert retrieved is not None
        # TODO: Assert retrieved['id'] == "123"
        assert retrieved['id'] == id
        # TODO: Assert retrieved['name'] == "John Doe"
        assert retrieved['name'] == name
        # TODO: Assert retrieved['email'] == "john@example.com"
        assert retrieved['email'] == email  

    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating a user with an invalid email raises."""
        # TODO: Use pytest.raises(ValueError, match="Invalid email")
        # TODO: Try to create a user with email="invalid-email"
        with pytest.raises(ValueError, match="Invalid email format"):
            user_repo.create_user("124", "Jane Doe", "invalid-email")   
    
    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that does not exist."""
        # TODO: Get the user with id="999"
        user = user_repo.get_user("999")
        # TODO: Assert the result is None
        assert user is None

    def test_database_not_connected_raises_error(self):
        """Test that operations fail when the database is not connected."""
        # TODO: Create a Database instance and do NOT connect it
        db = Database()
        # TODO: Create a UserRepository with this database
        user_repo = UserRepository(db)
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to create a user
        with pytest.raises(ConnectionError, match="Database not connected"):
            user_repo.create_user("125", "Alice", "alice@example.com")

    def test_get_on_disconnected_database_raises_error(self):
        """Test that reads fail too, not only writes."""
        # TODO: Create a UserRepository over an unconnected Database
        db = Database()
        user_repo = UserRepository(db)
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to read a user
        with pytest.raises(ConnectionError, match="Database not connected"):
            user_repo.get_user("123")
