"""Exercise 2: integration tests and fixtures with teardown."""

import pytest

from orderflow.users import Database, UserRepository


class TestUserRepositoryIntegration:
    """Integration tests for UserRepository against a real Database."""

    @pytest.fixture
    def database(self):
        """Provide a connected database, and close it again afterwards."""
        # TODO: Create a Database instance
        db=Database()
        # TODO: Call connect() on the database
        db.connect()
        # TODO: Use yield to hand the database to the test
        yield db
        # TODO: After the yield, call disconnect() on the database
        db.disconnect()
        #raise NotImplementedError("TODO: Implement this fixture")

    @pytest.fixture
    def user_repo(self, database):
        """Provide a UserRepository backed by the connected database."""
        # TODO: Create and return a UserRepository with the database fixture
        repo=UserRepository(database)
        return repo

    def test_create_and_retrieve_user(self, user_repo):
        """Test creating and then reading back a user."""
        # TODO: Create a user with id="123", name="John Doe", email="john@example.com"
        user=user_repo.create_user(user_id="123",name="John Doe",email="john@example.com")
        # TODO: Assert user['id'] == "123"
        assert user['id']=="123"
        # TODO: Assert user['name'] == "John Doe"
        assert user['name'] == "John Doe"
        # TODO: Assert user['email'] == "john@example.com"
        assert user['email'] == "john@example.com"
        # TODO: Assert 'created_at' is in user
        assert 'created_at' in user
        # TODO: Retrieve the user by id "123"
        retrieved_user=user_repo.get_user("123")
        # TODO: Assert the retrieved user is not None
        assert retrieved_user is not None
        # TODO: Assert retrieved['id'] == "123"
        assert retrieved_user["id"]=="123"
        # TODO: Assert retrieved['name'] == "John Doe"
        assert retrieved_user["name"]=="John Doe"

    def test_create_user_with_invalid_email(self, user_repo):
        """Test that creating a user with an invalid email raises."""
        # TODO: Use pytest.raises(ValueError, match="Invalid email")
        
        # TODO: Try to create a user with email="invalid-email"
        with pytest.raises(ValueError,match="Invalid email"):
            user_repo.create_user(user_id="11",name="noemail",email="john")
            

    def test_get_nonexistent_user(self, user_repo):
        """Test retrieving a user that does not exist."""
        # TODO: Get the user with id="999"
        # TODO: Assert the result is None
        assert user_repo.get_user(user_id="999") is None

    def test_database_not_connected_raises_error(self):
        """Test that operations fail when the database is not connected."""
        # TODO: Create a Database instance and do NOT connect it
        db=Database()
        # TODO: Create a UserRepository with this database
        user_repo=UserRepository(db)
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to create a user
        with pytest.raises(ConnectionError,match="not connected"):
            user_repo.create_user(user_id="1",name="John Doe",email="john@example.com")

    def test_get_on_disconnected_database_raises_error(self):
        """Test that reads fail too, not only writes."""
        # TODO: Create a UserRepository over an unconnected Database
        db=Database()
        user_repo=UserRepository(db)
        # TODO: Use pytest.raises(ConnectionError, match="not connected")
        # TODO: Try to read a user
        with pytest.raises(ConnectionError,match="not connected"):
            user_repo.get_user("123")
