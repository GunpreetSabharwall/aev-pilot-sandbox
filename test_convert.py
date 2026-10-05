"""Simple tests for convert.py. Run with: python -m pytest  (or: python test_convert.py)"""

import math

from convert import celsius_to_fahrenheit, fahrenheit_to_celsius


def test_freezing_point():
    assert celsius_to_fahrenheit(0) == 32
    assert fahrenheit_to_celsius(32) == 0


def test_boiling_point():
    assert celsius_to_fahrenheit(100) == 212
    assert fahrenheit_to_celsius(212) == 100


def test_minus_forty_is_the_same_on_both_scales():
    assert celsius_to_fahrenheit(-40) == -40
    assert fahrenheit_to_celsius(-40) == -40


def test_body_temperature():
    assert math.isclose(celsius_to_fahrenheit(37), 98.6)
    assert math.isclose(fahrenheit_to_celsius(98.6), 37)


def test_round_trip():
    for celsius in (-273.15, -12.5, 0, 21, 1000):
        assert math.isclose(fahrenheit_to_celsius(celsius_to_fahrenheit(celsius)), celsius, abs_tol=1e-9)


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
    print("All tests passed.")
