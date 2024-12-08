from . import count_one, valid_noun

funcs = [count_one.remover, valid_noun.remover]


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
