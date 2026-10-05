"""Convert temperatures between Celsius and Fahrenheit."""


def celsius_to_fahrenheit(celsius):
    """Return the Fahrenheit value for a temperature in Celsius."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    """Return the Celsius value for a temperature in Fahrenheit."""
    return (fahrenheit - 32) * 5 / 9
