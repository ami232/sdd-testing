"""Exercise 1a: unit tests for a pure function."""

import pytest

from orderflow.pricing import calculate_total_price


class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price."""

    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        price = 10.0
        quantity = 5

        result = calculate_total_price(price=price, quantity=quantity)

        assert result == 50

    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        price = 100.0
        quantity = 2
        discount = 10

        result = calculate_total_price(
            price = price,
            quantity=quantity,
            discount_percent=discount
        )

        assert result == float(200 - 20) # 180d

    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        price = 50.0
        quantity = 4
        discount = 50

        result = calculate_total_price(
            price = price,
            quantity=quantity,
            discount_percent=discount
        )

        assert result == float(200 - 100)

    def test_zero_quantity(self):
        """Test with zero quantity."""
        price = 10.0
        quantity = 0

        result = calculate_total_price(price = price, quantity=quantity)

        assert result == 0.0

    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        price = -10.0
        quantity = 5

        with pytest.raises(ValueError, match='must be non-negative'):
            calculate_total_price(price=price,quantity=quantity)

    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        price = 10.0
        quantity = -5

        with pytest.raises(ValueError, match='must be non-negative'):
            calculate_total_price(price=price,quantity=quantity)

    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        price = 10.0
        quantity = 5
        discount = 101

        with pytest.raises(ValueError, match='must be between 0 and 100'):
            calculate_total_price(price=price,quantity=quantity, discount_percent=discount)

    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""

        price = 10.0
        quantity = 5
        discount = -10

        with pytest.raises(ValueError, match='must be between 0 and 100'):
            calculate_total_price(price=price,quantity=quantity, discount_percent=discount)
