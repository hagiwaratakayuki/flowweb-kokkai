from collections import deque
from multiprocessing import Pool, TimeoutError
import time
import os
from multiprocessing.pool import Pool

from typing import TypedDict
import unittest
from unittest.mock import patch, MagicMock, call
import traceback
import asyncio


async def test():
    cor = asyncio.sleep(5)
    await cor
    print('ok')


async def asyncrunner():
    cors = deque()
    print('start')
    start = time.time()
    for i in range(1, 10 ** 5):
        cors.append(test())
    print(time.time() - start)
    start = time.time()
    await asyncio.gather(*cors)
    print(time.time() - start)


async def say_after(delay, what):
    print(what, f"started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(what)

asyncio.sleep


async def main():

    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

asyncio.run(main())


main()
"""
if __name__ == '__main__':
    # start 4 worker processes
    with Pool(5) as pool:
        imap = pool.imap_unordered(example, range(10))
"""
