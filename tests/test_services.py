"""
Exercises 3 and 4: replacing collaborators you do not want to call for real.

Nothing in this file may reach the network. If a test is slow or fails when
you are offline, something is still calling the real API.
"""

import pytest
from pytest_mock import mocker
import requests
from unittest.mock import Mock, patch

from orderflow.services import NotificationService, OrderProcessor, WeatherService


class TestWeatherServiceMocking:
    """Exercise 3: patch the HTTP layer the service depends on."""

    @patch("requests.get")
    def test_get_temperature_success(self, mock_get):
        """Test reading the temperature out of a mocked API response."""
        # TODO: Create a Mock() object for the response
        mock_response=Mock()
        # TODO: Set mock_response.json.return_value = {'temperature': 25.5}
        mock_response.json.return_value = {'temperature': 25.5}
        # TODO: Set mock_response.raise_for_status.return_value = None
        mock_response.raise_for_status.return_value = None
        # TODO: Set mock_get.return_value = mock_response
        mock_get.return_value = mock_response

        # TODO: Create a WeatherService with api_key="test"
        service=WeatherService(api_key="test")
        # TODO: Call get_temperature("London")
        temp=service.get_temperature("London")

        # TODO: Assert the temperature equals 25.5
        assert temp==25.5
        # TODO: Assert mock_get was called once with the right URL and params
        mock_get.assert_called_once()
        

    @patch("requests.get")
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        # TODO: Create a Mock() for the response
        mock_response=Mock()
        # TODO: Set the json return value with temperature: 25.0
        mock_response.json.return_value = {'temperature': 25.0}
        # TODO: Set mock_get.return_value
        mock_get.return_value = mock_response

        # TODO: Create a WeatherService instance
        service=WeatherService()
        # TODO: Call is_good_weather("Paris")
        result_service=service.is_good_weather("Paris")
        # TODO: Assert the result is True
        assert result_service is True

    @patch("requests.get")
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        # TODO: Create a mock response with temperature: 15.0
        mock_response=Mock()
        mock_response.json.return_value = {'temperature': 15.0}
        # TODO: Set mock_get.return_value
        mock_get.return_value=mock_response
        # TODO: Create a WeatherService instance
        service=WeatherService()
        # TODO: Call is_good_weather("Berlin")
        result_service=service.is_good_weather("Berlin")
        # TODO: Assert the result is False
        assert result_service==False

    @patch("requests.get")
    def test_api_error_handling(self, mock_get):
        """Test that an API failure propagates."""
        # TODO: Set mock_get.side_effect to raise requests.exceptions.RequestException
        mock_get.side_effect=requests.exceptions.RequestException

        # TODO: Create a WeatherService instance
        service=WeatherService()
        # TODO: Use pytest.raises to expect RequestException
        # TODO: Call get_temperature("Tokyo")
        with pytest.raises(requests.exceptions.RequestException):
            service.get_temperature("Tokyo")


class TestWeatherServiceConfig:
    """
    Exercise 3b: monkeypatch, for configuration a test must not depend on.

    monkeypatch is pytest's own patching fixture. It undoes every change it
    makes when the test ends, which is what keeps these tests independent.
    """

    def test_from_env_reads_api_key(self, monkeypatch):
        """Test that from_env picks up WEATHER_API_KEY."""
        # TODO: Use monkeypatch.setenv to set WEATHER_API_KEY to "key-from-env"
        monkeypatch.setenv("WEATHER_API_KEY", "key-from-env")
        # TODO: Build a service with WeatherService.from_env()
        service=WeatherService.from_env()
        # TODO: Assert service.api_key == "key-from-env"
        assert service.api_key == "key-from-env"

    def test_from_env_falls_back_to_demo_key(self, monkeypatch):
        """Test the default when the variable is not set at all."""
        # TODO: Use monkeypatch.delenv with raising=False to remove WEATHER_API_KEY
        monkeypatch.delenv("WEATHER_API_KEY", raising=False)
        # TODO: Build a service with WeatherService.from_env()
        service=WeatherService.from_env()
        # TODO: Assert service.api_key == "demo"
        assert service.api_key == "demo"


class TestOrderProcessorMocking:
    """Exercise 4: inject test doubles, and assert on how they were used."""

    def test_process_order_with_good_weather(self, customer_email):
        """Test order processing with both collaborators mocked."""
        # TODO: Create Mock(spec=WeatherService)
        weather_mocker=Mock(spec=WeatherService)
        # TODO: Set is_good_weather.return_value = True
        weather_mocker.is_good_weather.return_value=True

        # TODO: Create Mock(spec=NotificationService)
        notif_mocker=Mock(spec=NotificationService)
        # TODO: Set send_email.return_value = True
        notif_mocker.send_email.return_value=True

        # TODO: Create an OrderProcessor with both mocks
        order_processor=OrderProcessor(weather_service=weather_mocker, notification_service=notif_mocker)
        # TODO: Call process_order("ORD-001", customer_email, "Madrid")
        result=order_processor.process_order("ORD-001", customer_email, "Madrid")

        # TODO: Assert result['order_id'] == "ORD-001"
        # TODO: Assert result['notification_sent'] is True
        # TODO: Assert result['is_good_weather'] is True

        # TODO: Assert is_good_weather was called once with "Madrid"
        # TODO: Assert send_email was called once
        # TODO: Assert the email body contains "Enjoy the nice weather"
        assert False, "TODO: Implement this test"

    def test_process_order_with_bad_weather(self, customer_email):
        """Test order processing when the weather is bad."""
        # TODO: Create mocks for the weather and notification services
        # TODO: Set is_good_weather.return_value = False
        # TODO: Set send_email.return_value = True

        # TODO: Create an OrderProcessor and call process_order

        # TODO: Assert result['is_good_weather'] is False
        # TODO: Assert the email body does NOT contain "Enjoy the nice weather"
        assert False, "TODO: Implement this test"

    @patch.object(NotificationService, "send_email")
    @patch.object(WeatherService, "is_good_weather")
    def test_process_order_with_patch_object(self, mock_weather, mock_email):
        """
        Test the same flow by patching methods on the real classes.

        Note the argument order: decorators apply bottom-up, so the innermost
        decorator is the first parameter.
        """
        # TODO: Set mock_weather.return_value = True
        # TODO: Set mock_email.return_value = True

        # TODO: Create real WeatherService and NotificationService instances
        # TODO: Create an OrderProcessor with these instances
        # TODO: Call process_order("ORD-003", "test@example.com", "Barcelona")

        # TODO: Assert result['notification_sent'] is True
        # TODO: Assert mock_weather was called once with "Barcelona"
        # TODO: Assert mock_email was called once
        assert False, "TODO: Implement this test"

    def test_notification_failure_handling(self, customer_email):
        """Test what the result looks like when sending the email fails."""
        # TODO: Create mocks for the weather and notification services
        # TODO: Set is_good_weather.return_value = True
        # TODO: Set send_email.return_value = False (the email fails)

        # TODO: Create an OrderProcessor and call process_order

        # TODO: Assert result['notification_sent'] is False
        assert False, "TODO: Implement this test"


class TestNotificationServiceDirectly:
    """
    Exercise 4b: the real notification service, tested without a double.

    Mocks are for collaborators you cannot afford to call. This one is cheap,
    so calling it directly is both simpler and a stronger test.
    """

    def test_send_email_reports_success(self, capsys):
        """capsys is a pytest fixture that captures stdout during the test."""
        # TODO: Call NotificationService.send_email with any to/subject/body
        # TODO: Assert it returns True
        # TODO: Read the captured output with capsys.readouterr().out
        # TODO: Assert the output mentions the recipient you passed
        assert False, "TODO: Implement this test"
