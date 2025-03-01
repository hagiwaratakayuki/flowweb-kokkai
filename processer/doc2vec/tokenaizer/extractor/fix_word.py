from collections import defaultdict, deque
from typing import List, Any, Optional, Union
from ...util.specified_keyword import BindSpecifiedKeyword, SpecifiedKeyword
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

    def __call__(self, results: List[SpecifiedKeyword], parse_results: List, data) -> Any:
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
                results.append(SpecifiedKeyword(headword=result_word,
                                                is_force=self.is_force, source_ids=line_numbers, target_words=target_words))
        return results


class RegexExtractor:
    def __init__(self, word_pt: re.Pattern, result_words: Union[None, str, List[str]] = None, is_force=True, headword: Optional[str] = None) -> None:
        self.word_pt = word_pt
        if isinstance(result_words, str) == True:
            result_words = [result_words]

        self.result_words = result_words
        self.is_force = is_force
        self.headword = headword

    def __call__(self, results: List[SpecifiedKeyword], parse_results: List, data) -> Any:
        line_number = -1
        headword_to_line_numbers = defaultdict(deque)
        headword_to_haystacks = defaultdict(set)

        for line, tokens in parse_results:
            line_number += 1
            finds = self.word_pt.finditer(line)
            for find in finds:
                if self.result_words is not None:
                    headwords = tuple(self.result_words)
                    headword = self.headword or find.group(0)

                else:
                    headwords = None
                    headword = self.headword or find.group(0)
                key = (headwords, headword)
                headword_to_line_numbers[key].append(line_number)
                headword_to_haystacks[key].add(find.group(0))

        for key, line_numbers in headword_to_line_numbers.items():
            headwords, headword = key
            if headwords is None:
                results.append(SpecifiedKeyword(
                    headword=headword, is_force=self.is_force, source_ids=line_numbers))
            else:

                results.append(BindSpecifiedKeyword(
                    headwords=headwords, headword=headword, haystacks=headword_to_haystacks.get(key), is_force=self.is_force, line_numbers=line_numbers, is_fixed_headword=True))
        return results
