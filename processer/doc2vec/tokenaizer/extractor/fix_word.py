from collections import defaultdict, deque
from typing import List, Any, Optional, Union
from ...util.specific_keyword import SpecificKeyword
import re


class StringExtractor:
    def __init__(self, word: str, is_force=True) -> None:
        self.word = word
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        line_number = 0
        line_numbers = deque()
        is_found = False

        for line, tokens in parse_results:
            if self.word in line:
                is_found = True
                line_numbers.append(line_number)

            line_number += 1
        if is_found == True:

            results.append(SpecificKeyword(headword=self.word,
                           is_force=self.is_force, line_numbers=line_numbers))
        return results


class RegexExtractor:
    def __init__(self, word_pt: re.Pattern, result_words: Union[None, str, list] = None, is_force=True) -> None:
        self.word_pt = word_pt
        if isinstance(result_words, list) == False:
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
                headword=headword, is_force=self.is_force, target_word=target_word, line_numbers=line_numbers))

        return results
