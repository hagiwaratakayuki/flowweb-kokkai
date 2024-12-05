from collections import defaultdict, deque
from typing import List, Any, Optional, Union
from ...util.specific_keyword import SpecificKeyword
import re


class StringExtractor:
    def __init__(self, words: Union[str, List[str]], is_force=True, result_words: Union[None, str, List[str]] = None) -> None:
        if isinstance(words, str):
            words = [words]

        self.words = words
        if isinstance(result_words, str):
            result_words = [result_words]
        self.result_words = result_words
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        line_number = 0
        line_numbers = deque()
        is_found = False
        target_words = set()
        for line, tokens in parse_results:
            for word in self.words:
                if word in line:
                    is_found = True
                    line_numbers.append(line_number)
                    target_words.add(word)

            line_number += 1
        if is_found == True:
            for result_word in (self.result_words or self.words):
                results.append(SpecificKeyword(headword=result_word,
                                               is_force=self.is_force, line_numbers=line_numbers, target_words=target_words))
        return results


class RegexExtractor:
    def __init__(self, word_pt: re.Pattern, result_words: Union[None, str, List[str]] = None, is_force=True) -> None:
        self.word_pt = word_pt
        if isinstance(result_words, str) == True:
            result_words = [result_words]

        self.result_words = result_words
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        line_number = 0
        headword_to_line_numbers = defaultdict(deque)

        for line, tokens in parse_results:
            checked = self.word_pt.search(line)
            if checked is not None:
                if self.result_words is not None:
                    headwords = self.result_words
                    target_word = checked.group(0)
                else:
                    headwords = [checked.group(0)]
                    target_word = None
                for headword in headwords:

                    headword_to_line_numbers[(
                        headword, target_word)].append(line_number)
        for key, line_numbers in headword_to_line_numbers.items():
            headword, target_word = key
            results.append(SpecificKeyword(
                headword=headword, is_force=self.is_force, target_words=target_word, line_numbers=line_numbers))

        return results
