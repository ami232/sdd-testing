"""Bonus: the mock API itself, and the habits worth keeping."""

import pytest
from unittest.mock import Mock

from orderflow.services import WeatherService


class TestMockBestPractices:
    """Small, self-contained drills on Mock behaviour."""

    def test_using_spec_prevents_invalid_attributes(self):
        """A spec'd mock rejects attributes the real class does not have."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.get_temperature.return_value = 20.0

        with pytest.raises(AttributeError):
            mock_weather.non_existent_method()

    def test_verify_exact_calls_with_assert_called_with(self):
        """Verify the exact arguments a mock was called with."""
        mock_notification = Mock()
        mock_notification.send_email("test@example.com", "Subject", "Body")

        mock_notification.send_email.assert_called_with(
            "test@example.com", "Subject", "Body"
        )

    def test_verify_call_count(self):
        """Verify how many times a mock was called."""
        mock_service = Mock()

        mock_service.some_method()
        mock_service.some_method()
        mock_service.some_method()

        assert mock_service.some_method.call_count == 3

    def test_mock_side_effects(self):
        """Use side_effect for a different return value on each call."""
        mock_api = Mock()
        mock_api.fetch.side_effect = [10, 20, 30]

        assert mock_api.fetch() == 10
        assert mock_api.fetch() == 20
        assert mock_api.fetch() == 30

    def test_reset_mock(self):
        """Reset a mock to clear its call history."""
        mock_service = Mock()

        mock_service.method()
        assert mock_service.method.called is True

        mock_service.reset_mock()
        assert mock_service.method.called is False
