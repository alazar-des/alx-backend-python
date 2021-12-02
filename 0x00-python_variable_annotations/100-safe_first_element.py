#!/usr/bin/env python3
""" annonate a function. """
from typing import Sequence, Union, Any


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ safe first element. """
    if lst:
        return lst[0]
    else:
        return None
