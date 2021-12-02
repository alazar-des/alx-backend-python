#!/usr/bin/env python3
""" type-annonated sum of mixed list."""
from typing import Union, List


def sum_mixed_list(arr: List[Union[int, float]]) -> float:
    """ return sum of list of int and float. """
    return sum(arr)
