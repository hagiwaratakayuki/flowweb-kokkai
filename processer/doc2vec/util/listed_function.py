from typing import List, Callable


def invoke(funcs: List[Callable], results=None, *args, **kwargs):
    for func in funcs:
        results = func(results, *args, **kwargs)
    return results
