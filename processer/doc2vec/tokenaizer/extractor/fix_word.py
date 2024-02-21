from typing import List, Any
from ...util.specific_keyword import SpecificKeyword
import re


class StringExtractor:
    def __init__(self, word: str, is_force=True) -> None:
        self.word = word
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        for line, tokens in parse_results:
            if self.word in line:
                return SpecificKeyword(headword=self.word, is_force=self.is_force)


class RegexExtractor:
    def __init__(self, word_pt: re.Pattern, result_word=None, is_force=True) -> None:
        self.word_pt = word_pt
        self.result_word = result_word
        self.is_force = is_force

    def __call__(self, results: List[SpecificKeyword], parse_results: List, data) -> Any:
        for line, tokens in parse_results:
            checked = self.word_pt.search(line)
            if checked is not None:
                if self.result_word is not None:
                    headword = self.result_word
                else:
                    headword = checked.group(0)
                results.append(SpecificKeyword(
                    headword=headword, is_force=self.is_force, is_one_grame=True))

                return results
        return results
