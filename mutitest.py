from collections import deque
from functools import reduce
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


def check():
    r = []
    l = range(1000)

    start = time.perf_counter()
    for i in range(5):

        r.append(i)

    print(start - time.perf_counter())
    reducer = Reducer()
    start = time.perf_counter()
    [i for i in range(5)]
    print(start - time.perf_counter())


class Reducer:
    def __init__(self):
        self.value = 0

    def reduce(self, i):
        self.value += i


# check()
class T:
    a: int

    def __init__(self):
        a = 0


key = T()
tdict = {}
tdict[key] = 1
key.a = 3
print(tdict[T()])


# main()
"""
if __name__ == '__main__':
    # start 4 worker processes
    with Pool(5) as pool:
        imap = pool.imap_unordered(example, range(10))
"""
