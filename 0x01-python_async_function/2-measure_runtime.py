#!/usr/bin/env python3
"""
Measure average execution time
"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ Measure execution time."""
    loop = asyncio.get_event_loop()
    start_time = time.time()
    loop.run_until_complete(wait_n(n, max_delay))
    elapsed_time = time.time() - start_time
    return elapsed_time / n
