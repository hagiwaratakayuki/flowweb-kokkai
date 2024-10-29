from multiprocessing import Pool, TimeoutError
import time
import os
from multiprocessing.pool import Pool

from typing import TypedDict
import unittest
from unittest.mock import patch, MagicMock, call
import traceback


class Hoge:
    a: str


class Fuga(TypedDict, Hoge):
    pass


class MyTestCase(unittest.TestCase):
    def test_basic(self):
        with Pool() as pool:
            imap = pool.imap_unordered(example, range(10), chunksize=100)
            itr = test(imap)
            imap2 = pool.imap_unordered(example, itr, chunksize=100)
            t = [i for i in imap2]
            print(t)


class Fuga:
    t: int

    def test(self):
        class Hoge(type(self)):
            pass
        Hoge.__annotations__['c'] = str
        return Hoge()


print(__name__)


def example(i):
    print("ok")


def test(itr):
    for i in itr:
        yield i


def test2():
    return 1


def runner(pool):
    # print same numbers in arbitrary order
    for i in pool.imap_unordered(example, test(pool.imap_unordered(example, range(10)))):

        return 1, 2, 3, 4


"""
if __name__ == '__main__':
    # start 4 worker processes
    with Pool(5) as pool:
        imap = pool.imap_unordered(example, range(10))
"""
