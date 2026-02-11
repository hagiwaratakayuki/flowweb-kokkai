from collections import defaultdict

from operator import methodcaller
import re
from typing import Any, Iterable, List, Literal, Union, Optional

from data_loader.dto import DTO
from processor.doc2vec.base.protocol.keyword_extractor import ExtractResultDTO, KeywordExtractRule
from doc2vec.util.specified_keyword import BindSpecifiedKeyword, BindSpecifiedKeywordType, SpecifiedKeyword, SpecifiedKeywordType, BindSpecifiedKeywordType

OutputWord = Optional[Union[str, Iterable[str]]]
StartMethodCaller = methodcaller('start')


class RegexRule(KeywordExtractRule):
    patterns: Iterable[re.Pattern]
    output_word: OutputWord

    def __init__(self, patterns: Union[Iterable[re.Pattern], re.Pattern], output_word: OutputWord = None, is_bind_output=False, is_force=False, single_keyword_class: SpecifiedKeywordType = SpecifiedKeyword, bind_keyword_class: BindSpecifiedKeywordType = BindSpecifiedKeyword):
        try:
            iter(patterns)
            self.patterns = patterns

        except:
            self.patterns = [patterns]

        self.output_word = output_word
        self.single_keyword_class = single_keyword_class
        self.bind_keyword_class = bind_keyword_class
        self.is_bind_output = is_bind_output
        self._is_bind_fixed_output = output_word is not None and not isinstance(
            output_word, str)
        self._is_force = is_force

    def execute(self, parse_result, document_vector, sentiment_results, dto: DTO, results: ExtractResultDTO, postprocessor: Any):
        text = dto.get_text()

        all_matches: List[re.Match] = []

        for pt in self.patterns:
            all_matches.extend(pt.finditer(text))
        if not all_matches:
            return results
        if not self.output_word:
            headword_to_matches = defaultdict(list)
            for match in all_matches:
                headword = match.groups(0)
                headword_to_matches[headword].append(match)
            headword_to_tokens = defaultdict(set)
            for headword, matches in headword_to_matches.items():
                matches.sort(key=StartMethodCaller)
                headword_to_tokens[headword] = self._search_tokens(
                    parse_result=parse_result, matches=matches)
            if not self.is_bind_output:
                for headword, tokens in headword_to_tokens.items():
                    sk = self.single_keyword_class(
                        headword=headword, tokens=tokens, is_force=self._is_force)
                    results.add_keyword(sk)
            else:
                tokens = set()
                headwords = []
                for headword, _tokens in headword_to_tokens.items():
                    headwords.append(headword)
                    tokens.update(_tokens)
                sk = self.bind_keyword_class(
                    headwords=headwords, tokens=tokens, is_force=self._is_force)
                results.add_keyword(sk)
        else:
            all_matches.sort(key=StartMethodCaller)
            tokens = self._search_tokens(
                parse_result=parse_result, matches=all_matches)
            if self.is_bind_output:

                sk = self.bind_keyword_class(
                    headwords=self.output_word, source_ids=tokens)
                results.add_keyword(sk)
            else:
                sk = self.single_keyword_class(
                    headword=self.output_word, tokens=tokens)
                results.add_keyword(sk)
        return results

    def _search_tokens(self, parse_result, matches):
        pass
