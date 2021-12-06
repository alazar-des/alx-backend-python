#!/usr/bin/env python3
""" gather async function"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ call wait_random function n times."""
    lst = []
    aws = [task_wait_random(max_delay) for _ in range(n)]
    for coro in asyncio.as_completed(aws):
        lst.append(await coro)
    return lst
