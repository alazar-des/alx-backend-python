#!/usr/bin/env python3
""" return annonated function. """
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ return iteratable function. """
    return [(i, len(i)) for i in lst]
