from functools import reduce
from typing import Set

from doc2vec.base.keyword_extractor.rule.regex_rule import RegexRule
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from doc2vec.language.japanese.sudatchi.util.token_search import TokenSearcher


def reducer(a: Set, b: Set):

    return a | b


class SudatchiRegexRule(RegexRule):
    def _search_tokens(self, parse_result, matches):

        return reduce(reducer, TokenSearcher.search(matches=matches, dto=parse_result).values(), set())
