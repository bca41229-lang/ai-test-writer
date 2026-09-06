import pytest
from src.calculator import (
    add,
    subtract,
    multiply,
    divide,
    is_even,
    factorial,
    power,
)


class TestAdd:
    """测试 add 函数"""

    def test_add_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert add(-2, -3) == -5

    def test_add_mixed_signs(self):
        assert add(-2, 3) == 1

    def test_add_zero(self):
        assert add(0, 0) == 0
        assert add(5, 0) == 5
        assert add(0, 5) == 5

    def test_add_float_numbers(self):
        assert add(1.5, 2.5) == 4.0
        assert add(0.1, 0.2) == pytest.approx(0.3)

    def test_add_large_numbers(self):
        assert add(1e10, 1e10) == 2e10


class TestSubtract:
    """测试 subtract 函数"""

    def test_subtract_positive_numbers(self):
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        assert subtract(-5, -3) == -2

    def test_subtract_zero(self):
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5
        assert subtract(0, 0) == 0

    def test_subtract_float_numbers(self):
        assert subtract(5.5, 2.5) == 3.0
        assert subtract(0.3, 0.1) == pytest.approx(0.2)


class TestMultiply:
    """测试 multiply 函数"""

    def test_multiply_positive_numbers(self):
        assert multiply(2, 3) == 6

    def test_multiply_negative_numbers(self):
        assert multiply(-2, -3) == 6

    def test_multiply_mixed_signs(self):
        assert multiply(-2, 3) == -6

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0
        assert multiply(0, 5) == 0
        assert multiply(0, 0) == 0

    def test_multiply_by_one(self):
        assert multiply(5, 1) == 5
        assert multiply(1, 5) == 5

    def test_multiply_float_numbers(self):
        assert multiply(1.5, 2.0) == 3.0
        assert multiply(0.1, 0.2) == pytest.approx(0.02)


class TestDivide:
    """测试 divide 函数"""

    def test_divide_positive_numbers(self):
        assert divide(6, 3) == 2

    def test_divide_negative_numbers(self):
        assert divide(-6, -3) == 2

    def test_divide_mixed_signs(self):
        assert divide(-6, 3) == -2
        assert divide(6, -3) == -2

    def test_divide_result_is_float(self):
        assert divide(5, 2) == 2.5

    def test_divide_by_one(self):
        assert divide(5, 1) == 5

    def test_divide_zero_by_number(self):
        assert divide(0, 5) == 0

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="division by zero"):
            divide(5, 0)

    def test_divide_float_numbers(self):
        assert divide(5.5, 2.0) == pytest.approx(2.75)


class TestIsEven:
    """测试 is_even 函数"""

    def test_even_positive_number(self):
        assert is_even(2) is True
        assert is_even(4) is True

    def test_odd_positive_number(self):
        assert is_even(1) is False
        assert is_even(3) is False

    def test_zero_is_even(self):
        assert is_even(0) is True

    def test_even_negative_number(self):
        assert is_even(-2) is True
        assert is_even(-4) is True

    def test_odd_negative_number(self):
        assert is_even(-1) is False
        assert is_even(-3) is False

    def test_large_even_number(self):
        assert is_even(1000000) is True

    def test_large_odd_number(self):
        assert is_even(999999) is False


class TestFactorial:
    """测试 factorial 函数"""

    def test_factorial_zero(self):
        assert factorial(0) == 1

    def test_factorial_one(self):
        assert factorial(1) == 1

    def test_factorial_small_numbers(self):
        assert factorial(2) == 2
        assert factorial(3) == 6
        assert factorial(4) == 24
        assert factorial(5) == 120

    def test_factorial_large_number(self):
        assert factorial(10) == 3628800

    def test_factorial_negative_raises_error(self):
        with pytest.raises(ValueError, match="factorial of negative number"):
            factorial(-1)

    def test_factorial_negative_large_raises_error(self):
        with pytest.raises(ValueError, match="factorial of negative number"):
            factorial(-100)


class TestPower:
    """测试 power 函数"""

    def test_power_zero_exponent(self):
        assert power(5, 0) == 1
        assert power(0, 0) == 1

    def test_power_one_exponent(self):
        assert power(5, 1) == 5

    def test_power_positive_exponent(self):
        assert power(2, 3) == 8
        assert power(3, 2) == 9

    def test_power_base_zero(self):
        assert power(0, 5) == 0

    def test_power_negative_base(self):
        assert power(-2, 3) == -8
        assert power(-2, 2) == 4

    def test_power_float_base(self):
        assert power(1.5, 2) == pytest.approx(2.25)

    def test_power_large_exponent(self):
        assert power(2, 10) == 1024

    def test_power_negative_exponent_raises_error(self):
        with pytest.raises(ValueError, match="negative exponent not supported"):
            power(2, -1)

    def test_power_negative_exponent_large_raises_error(self):
        with pytest.raises(ValueError, match="negative exponent not supported"):
            power(2, -10)
