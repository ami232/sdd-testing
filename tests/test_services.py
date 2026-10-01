"""
Exercises 3 and 4: replacing collaborators you do not want to call for real.

Nothing in this file may reach the network. If a test is slow or fails when
you are offline, something is still calling the real API.
"""

import pytest
import requests
from unittest.mock import Mock, patch

from orderflow.services import NotificationService, OrderProcessor, WeatherService


def fake_response(temperature):
    """Build a mocked HTTP response carrying the given temperature."""
    response = Mock()
    response.json.return_value = {"temperature": temperature}
    response.raise_for_status.return_value = None
    return response


class TestWeatherServiceMocking:
    """Exercise 3: patch the HTTP layer the service depends on."""

    @patch("requests.get")
    def test_get_temperature_success(self, mock_get):
        """Test reading the temperature out of a mocked API response."""
        mock_get.return_value = fake_response(25.5)

        temperature = WeatherService(api_key="test").get_temperature("London")

        assert temperature == 25.5
        mock_get.assert_called_once_with(
            "https://api.weather.com/current",
            params={"city": "London", "key": "test"},
        )

    @patch("requests.get")
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        mock_get.return_value = fake_response(25.0)
        assert WeatherService().is_good_weather("Paris") is True

    @patch("requests.get")
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        mock_get.return_value = fake_response(15.0)
        assert WeatherService().is_good_weather("Berlin") is False

    @patch("requests.get")
    def test_is_good_weather_at_threshold_is_false(self, mock_get):
        """Exactly 20 degrees is not good weather: the check is strictly above."""
        mock_get.return_value = fake_response(20.0)
        assert WeatherService().is_good_weather("Lisbon") is False

    @patch("requests.get")
    def test_api_error_handling(self, mock_get):
        """Test that an API failure propagates."""
        mock_get.side_effect = requests.exceptions.RequestException("API down")
        with pytest.raises(requests.exceptions.RequestException, match="API down"):
            WeatherService().get_temperature("Tokyo")


class TestWeatherServiceConfig:
    """
    Exercise 3b: monkeypatch, for configuration a test must not depend on.

    monkeypatch is pytest's own patching fixture. It undoes every change it
    makes when the test ends, which is what keeps these tests independent.
    """

    def test_from_env_reads_api_key(self, monkeypatch):
        """Test that from_env picks up WEATHER_API_KEY."""
        monkeypatch.setenv("WEATHER_API_KEY", "key-from-env")
        assert WeatherService.from_env().api_key == "key-from-env"

    def test_from_env_falls_back_to_demo_key(self, monkeypatch):
        """Test the default when the variable is not set at all."""
        monkeypatch.delenv("WEATHER_API_KEY", raising=False)
        assert WeatherService.from_env().api_key == "demo"


def make_processor(good_weather, email_sent):
    """Build an OrderProcessor over spec'd doubles, returning all three."""
    weather = Mock(spec=WeatherService)
    weather.is_good_weather.return_value = good_weather
    notifier = Mock(spec=NotificationService)
    notifier.send_email.return_value = email_sent
    return OrderProcessor(weather, notifier), weather, notifier


class TestOrderProcessorMocking:
    """Exercise 4: inject test doubles, and assert on how they were used."""

    def test_process_order_with_good_weather(self, customer_email):
        """Test order processing with both collaborators mocked."""
        processor, weather, notifier = make_processor(True, True)

        result = processor.process_order("ORD-001", customer_email, "Madrid")

        assert result["order_id"] == "ORD-001"
        assert result["notification_sent"] is True
        assert result["is_good_weather"] is True
        weather.is_good_weather.assert_called_once_with("Madrid")
        notifier.send_email.assert_called_once()
        to, subject, body = notifier.send_email.call_args.args
        assert to == customer_email
        assert "Enjoy the nice weather" in body

    def test_process_order_with_bad_weather(self, customer_email):
        """Test order processing when the weather is bad."""
        processor, _, notifier = make_processor(False, True)

        result = processor.process_order("ORD-002", customer_email, "Oslo")

        assert result["is_good_weather"] is False
        body = notifier.send_email.call_args.args[2]
        assert "Enjoy the nice weather" not in body

    @patch.object(NotificationService, "send_email")
    @patch.object(WeatherService, "is_good_weather")
    def test_process_order_with_patch_object(self, mock_weather, mock_email):
        """
        Test the same flow by patching methods on the real classes.

        Note the argument order: decorators apply bottom-up, so the innermost
        decorator is the first parameter.
        """
        mock_weather.return_value = True
        mock_email.return_value = True
        processor = OrderProcessor(WeatherService(), NotificationService())

        result = processor.process_order("ORD-003", "test@example.com", "Barcelona")

        assert result["notification_sent"] is True
        mock_weather.assert_called_once_with("Barcelona")
        mock_email.assert_called_once()

    def test_notification_failure_handling(self, customer_email):
        """Test what the result looks like when sending the email fails."""
        processor, _, _ = make_processor(True, False)

        result = processor.process_order("ORD-004", customer_email, "Rome")

        assert result["notification_sent"] is False
        assert result["weather_checked"] is True


class TestNotificationServiceDirectly:
    """
    Exercise 4b: the real notification service, tested without a double.

    Mocks are for collaborators you cannot afford to call. This one is cheap,
    so calling it directly is both simpler and a stronger test.
    """

    def test_send_email_reports_success(self, capsys):
        """capsys is a pytest fixture that captures stdout during the test."""
        assert NotificationService.send_email("bob@example.com", "Hi", "Body") is True
        out = capsys.readouterr().out
        assert "bob@example.com" in out
        assert "Hi" in out
