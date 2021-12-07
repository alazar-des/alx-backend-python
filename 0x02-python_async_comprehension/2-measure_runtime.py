#!/usr/bin/env python3
""" Measure execution time. """
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ measure exection of 4 async_comprehension function running in parallel.
    """
    start_time = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    elapsed_time = time.time() - start_time
    return elapsed_time
