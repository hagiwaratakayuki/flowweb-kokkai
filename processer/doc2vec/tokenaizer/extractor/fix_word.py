from collections import defaultdict, deque
from typing import List, Any
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
    def __init__(self, word_pt: re.Pattern, result_word=None, is_force=True) -> None:
        self.word_pt = word_pt
        self.result_word = result_word
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        line_number = 0
        headword_to_line_nunmbers = defaultdict(deque)
        for line, tokens in parse_results:
            checked = self.word_pt.search(line)
            if checked is not None:
                if self.result_word is not None:
                    headword = self.result_word
                else:
                    headword = checked.group(0)
                headword_to_line_nunmbers[headword].append(line_number)
        for headword, line_numbers in headword_to_line_nunmbers.items():
            results.append(SpecificKeyword(
                headword=headword, is_force=self.is_force, is_one_grame=True, line_numbers=line_numbers))

        return results
