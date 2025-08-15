from collections import defaultdict
from operator import methodcaller
import re
from typing import List

from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
StartColler = methodcaller('start')  # for sort


class Searcher:
    def search(self, matches: List[re.Match], dto: SudatchiDTO):
        token_len = dto.get_tokens_len()
        token_index = 0
        results = defaultdict(set)

        for m in matches:

            while token_index < token_len:
                token = dto.tokens[token_index]
                if token.end() <= m.start():
                    token_index += 1
                    continue
                if token.end() == m.end():
                    results[m].add(token)
                    token_index += 1
                    break
                if token.end() > m.end():
                    if m.start() <= token.begin() < m.end():
                        results[m].add(token)
                        token_index += 1
                        continue
                    if token.begin() != m.end():
                        token_index += 1
                    break
                token_index += 1
                results[m].add(token)

        return results

# duck type re.match


class PseudoMatch:
    def __init__(self, word, start):
        self._word = word
        self._start = start
        self._end = len(word)

    def group(self, number):
        return self._word


TokenSearcher = Searcher()
