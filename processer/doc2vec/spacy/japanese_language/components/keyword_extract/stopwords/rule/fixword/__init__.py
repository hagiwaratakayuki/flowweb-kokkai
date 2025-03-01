
removers = []


def fix_remover(words):
    for remover in removers:
        words = remover(words)
    return words
