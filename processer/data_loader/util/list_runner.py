def run(funcs, text, data):

    for func in funcs:

        text = func(text, data)

    return text
