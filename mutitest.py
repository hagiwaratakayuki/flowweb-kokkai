from multiprocessing import Pool, TimeoutError
import time
import os


class Hoge:
    pass


class Fuga:
    t: int

    def test(self):
        class Hoge(type(self)):
            pass
        Hoge.__annotations__['c'] = str
        return Hoge()


Fuga().test().c


def example(x):
    return x * 2


def test(itr):
    for i in itr:
        yield i


def test2(pool: Pool):
    return


def runner(pool):
    # print same numbers in arbitrary order
    for i in pool.imap_unordered(example, test(pool.imap_unordered(example, range(10)))):
        print(i)
        return 1, 2, 3, 4


"""
if __name__ == '__main__':
    # start 4 worker processes
    with Pool(5) as pool:
        runner(pool=pool)
"""


def test3(flag):
    if flag:
        for i in [1]:
            yield i


print(list(test3(False)))
