#!/usr/bin/env python3
""" gather async function"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ call wait_random function n times."""
    lst = []
    aws = [wait_random(max_delay) for _ in range(n)]
    for coro in asyncio.as_completed(aws):
        lst.append(await coro)
    return lst
