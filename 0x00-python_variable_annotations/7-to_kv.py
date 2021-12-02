#!/usr/bin/env python3
""" type-annonated module which created a tuple."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """ convet str and int or float to tuple of str and float. """
    return (k, v ** 2)
