from .list_remover import list_remover
from .rule.preg import preg_remover
from .rule.function_remover import fu
from typing import List

removers = [
    list_remover,
    preg_remover

]


def remove_stopwords(words: List[str]) -> List[str]:

    for remover in removers:
        words = remover(words)
    return words
