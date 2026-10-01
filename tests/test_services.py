"""
Exercises 3 and 4: replacing collaborators you do not want to call for real.

Nothing in this file may reach the network. If a test is slow or fails when
you are offline, something is still calling the real API.
"""

import pytest
import requests
from unittest.mock import Mock, patch

from orderflow.services import NotificationService, OrderProcessor, WeatherService


def make_response(temperature: float) -> Mock:
    """Build a fake requests.Response that reports the given temperature."""
    response = Mock()
    response.json.return_value = {"temperature": temperature}
    response.raise_for_status.return_value = None
    return response


class TestWeatherServiceMocking:
    """Exercise 3: patch the HTTP layer the service depends on."""

    @patch("requests.get")
    def test_get_temperature_success(self, mock_get):
        """Test reading the temperature out of a mocked API response."""
        mock_response = Mock()
        mock_response.json.return_value = {"temperature": 25.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = WeatherService(api_key="test")
        temperature = service.get_temperature("London")

        assert temperature == 25.5
        mock_get.assert_called_once_with(
            "https://api.weather.com/current",
            params={"city": "London", "key": "test"},
        )
        mock_response.raise_for_status.assert_called_once()

    @patch("requests.get")
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        mock_get.return_value = make_response(25.0)

        service = WeatherService()
        assert service.is_good_weather("Paris") is True

    @patch("requests.get")
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        mock_get.return_value = make_response(15.0)

        service = WeatherService()
        assert service.is_good_weather("Berlin") is False

    @patch("requests.get")
    def test_is_good_weather_exactly_20_is_not_good(self, mock_get):
        """Test the boundary: the threshold is strictly greater than 20."""
        mock_get.return_value = make_response(20.0)

        service = WeatherService()
        assert service.is_good_weather("Lisbon") is False

    @patch("requests.get")
    def test_api_error_handling(self, mock_get):
        """Test that an API failure propagates."""
        mock_get.side_effect = requests.exceptions.RequestException("API down")

        service = WeatherService()
        with pytest.raises(requests.exceptions.RequestException, match="API down"):
            service.get_temperature("Tokyo")

    @patch("requests.get")
    def test_http_error_status_propagates(self, mock_get):
        """Test that a non-2xx response raises instead of returning garbage."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error"
        )
        mock_get.return_value = mock_response

        service = WeatherService()
        with pytest.raises(requests.exceptions.HTTPError, match="500"):
            service.get_temperature("Tokyo")
        mock_response.json.assert_not_called()


class TestWeatherServiceConfig:
    """
    Exercise 3b: monkeypatch, for configuration a test must not depend on.

    monkeypatch is pytest's own patching fixture. It undoes every change it
    makes when the test ends, which is what keeps these tests independent.
    """

    def test_from_env_reads_api_key(self, monkeypatch):
        """Test that from_env picks up WEATHER_API_KEY."""
        monkeypatch.setenv("WEATHER_API_KEY", "key-from-env")
        service = WeatherService.from_env()
        assert service.api_key == "key-from-env"

    def test_from_env_falls_back_to_demo_key(self, monkeypatch):
        """Test the default when the variable is not set at all."""
        monkeypatch.delenv("WEATHER_API_KEY", raising=False)
        service = WeatherService.from_env()
        assert service.api_key == "demo"


class TestOrderProcessorMocking:
    """Exercise 4: inject test doubles, and assert on how they were used."""

    def test_process_order_with_good_weather(self, customer_email):
        """Test order processing with both collaborators mocked."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = True

        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = True

        processor = OrderProcessor(mock_weather, mock_notification)
        result = processor.process_order("ORD-001", customer_email, "Madrid")

        assert result["order_id"] == "ORD-001"
        assert result["notification_sent"] is True
        assert result["weather_checked"] is True
        assert result["is_good_weather"] is True

        mock_weather.is_good_weather.assert_called_once_with("Madrid")
        mock_notification.send_email.assert_called_once()
        to, subject, body = mock_notification.send_email.call_args.args
        assert to == customer_email
        assert subject == "Order Confirmation"
        assert "ORD-001" in body
        assert "Enjoy the nice weather" in body

    def test_process_order_with_bad_weather(self, customer_email):
        """Test order processing when the weather is bad."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = False
        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = True

        processor = OrderProcessor(mock_weather, mock_notification)
        result = processor.process_order("ORD-002", customer_email, "Oslo")

        assert result["is_good_weather"] is False
        mock_notification.send_email.assert_called_once_with(
            customer_email, "Order Confirmation", "Order ORD-002 confirmed!"
        )
        body = mock_notification.send_email.call_args.args[2]
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
        assert result["is_good_weather"] is True
        mock_weather.assert_called_once_with("Barcelona")
        mock_email.assert_called_once()
        assert "Enjoy the nice weather" in mock_email.call_args.args[2]

    def test_notification_failure_handling(self, customer_email):
        """Test what the result looks like when sending the email fails."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.return_value = True
        mock_notification = Mock(spec=NotificationService)
        mock_notification.send_email.return_value = False

        processor = OrderProcessor(mock_weather, mock_notification)
        result = processor.process_order("ORD-004", customer_email, "Rome")

        assert result["notification_sent"] is False
        assert result["order_id"] == "ORD-004"
        assert result["weather_checked"] is True
        mock_notification.send_email.assert_called_once()

    def test_weather_failure_skips_notification(self, customer_email):
        """Test that an exception from the weather service stops the flow."""
        mock_weather = Mock(spec=WeatherService)
        mock_weather.is_good_weather.side_effect = requests.exceptions.RequestException
        mock_notification = Mock(spec=NotificationService)

        processor = OrderProcessor(mock_weather, mock_notification)
        with pytest.raises(requests.exceptions.RequestException):
            processor.process_order("ORD-005", customer_email, "Cairo")
        mock_notification.send_email.assert_not_called()


class TestNotificationServiceDirectly:
    """
    Exercise 4b: the real notification service, tested without a double.

    Mocks are for collaborators you cannot afford to call. This one is cheap,
    so calling it directly is both simpler and a stronger test.
    """

    def test_send_email_reports_success(self, capsys, customer_email):
        """capsys is a pytest fixture that captures stdout during the test."""
        assert NotificationService.send_email(customer_email, "Hello", "Body") is True

        out = capsys.readouterr().out
        assert customer_email in out
        assert "Hello" in out
