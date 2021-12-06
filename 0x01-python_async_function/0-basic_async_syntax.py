#!/usr/bin/env python3
""" async function. """
import asyncio
import random


async def wait_random(max_delay=10):
    """ async funcion that waits asyncly betweet 0 and max_delay."""
    random_delay = random.uniform(0, max_delay)
    await asyncio.sleep(random_delay)
    return random_delay
