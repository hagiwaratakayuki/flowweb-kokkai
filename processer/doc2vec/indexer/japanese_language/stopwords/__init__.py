removers = [

]


def remove_stopwords(words):
    for remover in removers:
        words = remover(words)
