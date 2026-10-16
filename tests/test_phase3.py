import pytest

from drico_bot.calc.safe_eval import SafeCalcError, safe_calculate


def test_calculator_precedence():
    assert safe_calculate("2+3*4") == 14


def test_zero_division():
    assert safe_calculate("10/0") == "Error: cannot divide by 0"


def test_reject_import():
    with pytest.raises(SafeCalcError):
        safe_calculate("__import__('os')")


def test_reject_dunder_class():
    with pytest.raises(SafeCalcError):
        safe_calculate("(1).__class__")


def test_reject_huge_exponent():
    with pytest.raises(SafeCalcError):
        safe_calculate("10**200")


def test_sqrt_and_constants():
    assert safe_calculate("round(sqrt(pi), 2)") == round(3.141592653589793 ** 0.5, 2)
