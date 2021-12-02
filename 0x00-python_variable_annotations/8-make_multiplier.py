#!/usr/bin/env python3
""" a module that return annonated function. """
from typing import Callable


def func(mul: float) -> float:
    """ return square of mul. """
    return mul * mul


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ return a callable. """
    return func
