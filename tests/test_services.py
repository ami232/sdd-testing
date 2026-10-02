"""
Exercises 3 and 4: replacing collaborators you do not want to call for real.

Nothing in this file may reach the network. If a test is slow or fails when
you are offline, something is still calling the real API.
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock

from orderflow.services import NotificationService, OrderProcessor, WeatherService


class TestWeatherServiceMocking:
    """Exercise 3: patch the HTTP layer the service depends on."""

    @patch("requests.get")
    def test_get_temperature_success(self, mock_get: MagicMock):
        """Test reading the temperature out of a mocked API response."""

        city = 'London'
        api_key = 'test'
        
        mock_response = Mock()

        mock_response.json.return_value = {'temperature': 25.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        weather_service = WeatherService(
            api_key=api_key
        )

        temperature = weather_service.get_temperature(city=city)

        assert temperature == 25.5

        mock_get.assert_called_once_with(
            'https://api.weather.com/current',
            params = {
                'city': city,
                'key': api_key
            }
        )

    @patch("requests.get")
    def test_is_good_weather_true(self, mock_get):
        """Test good weather detection (temp > 20)."""
        city = 'Paris'
        api_key = 'test'
        
        mock_response = Mock()

        mock_response.json.return_value = {'temperature': 25.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        weather_service = WeatherService(
            api_key=api_key
        )

        is_good_weather = weather_service.is_good_weather(city=city)

        assert is_good_weather == True

    @patch("requests.get")
    def test_is_good_weather_false(self, mock_get):
        """Test bad weather detection (temp <= 20)."""
        city    = 'Berlin'
        api_key = 'test'
        
        mock_response = Mock()

        mock_response.json.return_value = {'temperature': 15.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        weather_service = WeatherService(
            api_key=api_key
        )

        is_good_weather = weather_service.is_good_weather(city=city)

        assert is_good_weather == False

    @patch("requests.get")
    def test_api_error_handling(self, mock_get: MagicMock):
        """Test that an API failure propagates."""

        mock_get.side_effect  = requests.exceptions.RequestException(
            "API unavailable"
        )

        service = WeatherService(api_key='test')

        with pytest.raises(
            requests.exceptions.RequestException, match="API unavailable"
        ):
            service.get_temperature("Tokyo")

    @patch('requests.get')
    def test_is_good_weather_at_twenty_is_false(self, mock_get):
        response = Mock()
        response.json.return_value = {'temperature': 20.0}
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        service = WeatherService(api_key='test')

        assert service.is_good_weather("Berlin") is False

class TestWeatherServiceConfig:
    """
    Exercise 3b: monkeypatch, for configuration a test must not depend on.

    monkeypatch is pytest's own patching fixture. It undoes every change it
    makes when the test ends, which is what keeps these tests independent.
    """

    def test_from_env_reads_api_key(self, monkeypatch):
        """Test that from_env picks up WEATHER_API_KEY."""
        monkeypatch.setenv(
            name = 'WEATHER_API_KEY',
            value = 'key-from-env'
        )

        service = WeatherService.from_env()

        assert service.api_key == 'key-from-env'

    def test_from_env_falls_back_to_demo_key(self, monkeypatch):
        """Test the default when the variable is not set at all."""

        monkeypatch.delenv(
            name='WEATHER_API_KEY',
            raising=False
        )

        service = WeatherService.from_env()

        assert service.api_key == 'demo'

class TestOrderProcessorMocking:
    """Exercise 4: inject test doubles, and assert on how they were used."""

    def test_process_order_with_good_weather(self, customer_email):
        """Test order processing with both collaborators mocked."""

        weather = Mock(spec=WeatherService)
        weather.is_good_weather.return_value = True

        notification = Mock(spec=NotificationService)
        notification.send_email.return_value = True

        processor = OrderProcessor(weather, notification)
        result = processor.process_order(
            'ORD-001',
            customer_email,
            'Madrid'
        )

        assert result['order_id'] == "ORD-001"
        assert result['notification_sent'] is True
        assert result['is_good_weather'] is True

        weather.is_good_weather.assert_called_once_with('Madrid')
        notification.send_email.assert_called_once()

        _, _,  body = notification.send_email.call_args.args

        assert 'Enjoy the nice weather' in body

    def test_process_order_with_bad_weather(self, customer_email):
        """Test order processing when the weather is bad."""

        weather = Mock(spec=WeatherService)
        weather.is_good_weather.return_value = False

        notification = Mock(spec=NotificationService)
        notification.send_email.return_value = True

        processor = OrderProcessor(weather, notification)
        result = processor.process_order(
            'ORD-002',
            customer_email,
            'Berlin'
        )

        assert result['is_good_weather'] is False
        _, _,  body = notification.send_email.call_args.args

        assert 'Enjoy the nice weather' not in body

    @patch.object(NotificationService, "send_email")
    @patch.object(WeatherService, "is_good_weather")
    def test_process_order_with_patch_object(self, mock_weather, mock_email):
        mock_weather.return_value = True
        mock_email.return_value = True

        weather = WeatherService()
        notification = NotificationService()

        processor = OrderProcessor(weather, notification)
        result = processor.process_order(
            'ORD-003',
            'test@example.com',
            'Barcelona'
        )

        assert result['notification_sent'] is True

        mock_weather.assert_called_once_with('Barcelona')
        mock_email.assert_called_once()

    def test_notification_failure_handling(self, customer_email):
        """Test what the result looks like when sending the email fails."""
        weather = Mock(spec=WeatherService)
        weather.is_good_weather.return_value = True

        notification = Mock(spec=NotificationService)
        notification.send_email.return_value = False

        processor = OrderProcessor(weather, notification)
        result = processor.process_order(
            'ORD-004',
            customer_email,
            'Madrid'
        )

        assert result['notification_sent'] is False

class TestNotificationServiceDirectly:
    """
    Exercise 4b: the real notification service, tested without a double.

    Mocks are for collaborators you cannot afford to call. This one is cheap,
    so calling it directly is both simpler and a stronger test.
    """

    def test_send_email_reports_success(self, capsys):
        """capsys is a pytest fixture that captures stdout during the test."""
        email = 'test@example.com'

        sent = NotificationService.send_email(
            to=email,
            subject='Test',
            body='Test body'
        )

        assert sent is True

        captured = capsys.readouterr().out

        assert email in captured
