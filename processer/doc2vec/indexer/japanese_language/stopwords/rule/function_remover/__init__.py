from .count_one import count_one
from .valid_noun import valid_noun

funcs = [count_one, valid_noun]


def function_remover(words):
    ret = []
    for word in words:
        is_valid = True
        for func in funcs:
            if func(word) == True:
                is_valid = False
                break
        if is_valid == False:
            continue
        ret.append(word)
    return ret
