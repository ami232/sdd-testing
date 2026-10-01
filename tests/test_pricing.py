"""Exercise 1a: unit tests for a pure function."""

import pytest

from orderflow.pricing import calculate_total_price


class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price."""

    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        result = calculate_total_price(price=10.0, quantity=5)
        assert result == 50.0

    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        result = calculate_total_price(
            price=100.0, quantity=2, discount_percent=10
        )
        assert result == 180.0

    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        result = calculate_total_price(
            price=50.0, quantity=4, discount_percent=50
        )
        assert result == 100.0

    def test_zero_quantity(self):
        """Test with zero quantity."""
        result = calculate_total_price(price=10.0, quantity=0)
        assert result == 0.0

    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price=-10.0, quantity=5)

    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(price=10.0, quantity=-5)

    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=101)

    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=-10)
