
from typing import List

removers = [

]


def remove_stopwords(words: List[str]) -> List[str]:

    for remover in removers:
        words = remover(words)
    return words
