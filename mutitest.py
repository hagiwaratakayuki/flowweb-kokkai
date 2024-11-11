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
    await asyncio.sleep(1)


async def asyncrunner():
    cors = deque()
    print('start')
    start = time.time()
    for i in range(1, 10 ** 5):
        cors.append(test())
    print(time.time() - start)
    await asyncio.gather(*cors)


def main():
    asyncio.run(asyncrunner())


main()
"""
if __name__ == '__main__':
    # start 4 worker processes
    with Pool(5) as pool:
        imap = pool.imap_unordered(example, range(10))
"""
