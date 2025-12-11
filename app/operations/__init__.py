# app/operations.py

"""
Module: operations.py

This module contains basic arithmetic functions that perform addition, subtraction,
multiplication, division, and exponentiation of two numbers. These functions are
used by the calculator API to compute results based on user input.

Functions:
- add(a, b) -> sum of a and b
- subtract(a, b) -> difference of a and b
- multiply(a, b) -> product of a and b
- divide(a, b) -> quotient of a / b (error if b == 0)
- power(a, b) -> a raised to the power of b
"""

from typing import Union 

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers and return the result."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Subtract the second number from the first."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers and return the product."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Divide the first number by the second. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def power(a: Number, b: Number) -> Number:
    """Raise a to the power of b (a^b)."""
    return a ** b
