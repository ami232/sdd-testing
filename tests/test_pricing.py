"""Exercise 1a: unit tests for a pure function."""

import pytest

from orderflow.pricing import calculate_total_price


class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price."""

    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        # TODO: Call calculate_total_price with price=10.0, quantity=5
        # TODO: Assert the result equals 50.0
        #arrange
        price = 10.0
        quantity = 5
        #act
        result = calculate_total_price(price, quantity)
        #assert
        assert result == 50.0

    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        # TODO: Call calculate_total_price with price=100.0, quantity=2, discount=10
        # TODO: Assert the result equals 180.0 (200 - 20)
        #arrange
        price = 100.0
        quantity = 2
        discount_percent = 10
        #act
        result = calculate_total_price(price, quantity, discount_percent)
        #assert
        assert result == 180.0

    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        # TODO: Call calculate_total_price with price=50.0, quantity=4, discount=50
        # TODO: Assert the result equals 100.0 (200 - 100)
        #arrange
        price = 50.0
        quantity = 4
        discount_percent = 50
        #act
        result = calculate_total_price(price, quantity, discount_percent)
        #assert
        assert result == 100.0

    def test_zero_quantity(self):
        """Test with zero quantity."""
        # TODO: Call calculate_total_price with price=10.0, quantity=0
        # TODO: Assert the result equals 0.0
        #arrange
        price = 10.0
        quantity = 0
        #act
        result = calculate_total_price(price, quantity)
        #assert
        assert result == 0.0

    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be non-negative")
        # TODO: Call calculate_total_price with price=-10.0, quantity=5
        #arrange
        price = -10.0
        quantity = 5
        #act
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price, quantity)

    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be non-negative")
        # TODO: Call calculate_total_price with price=10.0, quantity=-5
        #arrange
        price = 10.0
        quantity = -5
        #act
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price, quantity)

    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be between 0 and 100")
        # TODO: Call calculate_total_price with discount=101
        #arrange
        discount_percent = 101
        #act
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price, quantity, discount_percent)

    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""
        # TODO: Use pytest.raises(ValueError, match="must be between 0 and 100")
        # TODO: Call calculate_total_price with discount=-10
        #arrange
        discount_percent = -10
        #act
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price, quantity, discount_percent)
