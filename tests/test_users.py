"""Exercise 2: integration tests and fixtures with teardown."""

import pytest

from orderflow.users import Database, UserRepository


class TestUserRepositoryIntegration:
    """Integration tests for UserRepository against a real Database."""

    @pytest.fixture
    def database(self):
        db = Database()
        db.connect()
        yield db
        db.disconnect()

    @pytest.fixture
    def user_repo(self, database):
        return UserRepository(database)

    def test_create_and_retrieve_user(self, user_repo):
        user = user_repo.create_user("123", "John Doe", "john@example.com")
        user['id'] == "123"
        user['name'] == "John Doe"
        user['email'] == "john@example.com"
        assert 'created_at' in user

        retrieved = user_repo.get_user("123")
        assert retrieved is not None
        assert retrieved['id'] == "123"
        assert retrieved['name'] == "John Doe"

    def test_create_user_with_invalid_email(self, user_repo):
        with pytest.raises(ValueError, match="Invalid email"):
            user_repo.create_user("123", "John Doe", "invalid-email")

    def test_get_nonexistent_user(self, user_repo):
        assert user_repo.get_user("999") is None

    def test_database_not_connected_raises_error(self):
        repo = UserRepository(Database())
        with pytest.raises(ConnectionError, match="not connected"):
            repo.create_user("123", "John Doe", "john@example.com")

    def test_get_on_disconnected_database_raises_error(self):
        repo = UserRepository(Database())
        with pytest.raises(ConnectionError, match="not connected"):
            repo.create_user("123", "John Doe", "john@example.com")
