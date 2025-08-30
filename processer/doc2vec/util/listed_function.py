from typing import List, Callable


def true_break(funcs: List[Callable], *args, **kwargs):
    for func in funcs:
        if func(*args, **kwargs) == True:
            return True
    return False
