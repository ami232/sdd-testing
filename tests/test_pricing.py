"""Exercise 1a: unit tests for a pure function."""

import pytest

from orderflow.pricing import calculate_total_price


class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price."""

    def test_basic_calculation_no_discount(self):
        """Test basic price calculation without discount."""
        assert calculate_total_price(10.0, 5) == 50.0

    def test_calculation_with_discount(self):
        """Test price calculation with discount."""
        assert calculate_total_price(100.0, 2, discount_percent=10) == 180.0

    def test_calculation_with_50_percent_discount(self):
        """Test with 50% discount."""
        assert calculate_total_price(50.0, 4, discount_percent=50) == 100.0

    def test_zero_quantity(self):
        """Test with zero quantity."""
        assert calculate_total_price(10.0, 0) == 0.0

    def test_zero_price(self):
        """Test that a free item costs nothing regardless of quantity."""
        assert calculate_total_price(0.0, 7) == 0.0

    def test_full_discount_boundary(self):
        """Test that a 100% discount is allowed and makes the order free."""
        assert calculate_total_price(10.0, 3, discount_percent=100) == 0.0

    def test_zero_discount_boundary(self):
        """Test that an explicit 0% discount equals no discount."""
        assert calculate_total_price(10.0, 3, discount_percent=0) == 30.0

    def test_fractional_discount(self):
        """Test a non-integer discount with float-safe comparison."""
        assert calculate_total_price(19.99, 3, discount_percent=12.5) == pytest.approx(
            52.47375
        )

    def test_negative_price_raises_error(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(-10.0, 5)

    def test_negative_quantity_raises_error(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculate_total_price(10.0, -5)

    def test_invalid_discount_over_100(self):
        """Test that discount over 100 raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(10.0, 5, discount_percent=101)

    def test_invalid_discount_negative(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            calculate_total_price(10.0, 5, discount_percent=-10)
