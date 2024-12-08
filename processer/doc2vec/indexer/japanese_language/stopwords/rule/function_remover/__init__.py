from .count_one import count_one
from .valid_noun import valid_noun

funcs = [count_one, valid_noun]


def function_remover(words):
    ret = []
    for word in words:
        is_break = False
        for func in funcs:
            if func(word) == True:
                is_break = True
                break
        if is_break:
            break
        ret.append(word)
    return ret
