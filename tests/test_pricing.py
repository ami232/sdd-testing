"""Exercise 1a: unit tests for a pure function."""

import pytest

from orderflow.pricing import calculate_total_price


class TestCalculateTotalPrice:
    """Unit tests for calculate_total_price."""

    def test_basic_calculation_no_discount(self):
        assert calculate_total_price(price = 10.0, quantity = 5) == 50.0

    def test_calculation_with_discount(self):
        assert calculate_total_price(price = 100.0, quantity = 2, discount_percent=10) == 180.0

    def test_calculation_with_50_percent_discount(self):
        assert calculate_total_price(price=50.0, quantity= 4, discount_percent=50) == 100.0

    def test_zero_quantity(self):
        assert calculate_total_price(price=10, quantity=0) == 0.0

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price and quantity must be non-negative"):
            calculate_total_price(price=-10.0, quantity=5)

    def test_negative_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Price and quantity must be non-negative"):
            calculate_total_price(price=10.0, quantity=-5)

    def test_invalid_discount_over_100(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=101)

    def test_invalid_discount_negative(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_total_price(price=10.0, quantity=5, discount_percent=-10)
