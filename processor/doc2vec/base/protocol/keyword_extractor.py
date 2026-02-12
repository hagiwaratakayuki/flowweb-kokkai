from abc import ABCMeta, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Optional, Set, Union
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO
from doc2vec.base.protocol.sentiment import SentimentResult

from doc2vec.base.protocol.postprocessor import DocVectorType, KeywordsType
from doc2vec.util.specified_keyword import SpecifiedKeyword

SpecifiedKeyword
type Token2Keyword = Dict[Token, Set[SpecifiedKeyword]]


EMPTY_SET = set()


class ExtractResultDTO:
    source_2_keyword: Token2Keyword
    keywords: Set[SpecifiedKeyword]

    def __init__(self):
        self.source_2_keyword = defaultdict(set)

        self.keywords = set()

    def add_keyword(self, keyword: SpecifiedKeyword, is_overwrite_token=True):

        self.keywords.add(keyword)
        if is_overwrite_token == True:

            for target_keyword in self.get_by_source_ids(keyword.tokens):

                target_keyword.tokens -= keyword.tokens

        for source_id in keyword.tokens:
            self.source_2_keyword[source_id].add(keyword)

    def remove_kewywords(self, source_ids):

        for kw in self.get_by_source_ids(source_ids=source_ids):

            kw.tokens -= source_ids

    def get_keywords(self):
        # refarence shortcut
        return [keyword for keyword in self.keywords if keyword.tokens != EMPTY_SET]

    def get_by_source_ids(self, source_ids: Iterable[Any]) -> Set[SpecifiedKeyword]:
        ret: Set[SpecifiedKeyword] = set()
        for source_id in source_ids:
            ret.update(self.source_2_keyword.get(source_id, []))
        return ret

    def check_by_source_ids(self, source_ids):
        return {source_id for source_id in source_ids if source_id in self.source_2_keyword}

    def substruct_sorce_id(self, keyword: SpecifiedKeyword, source_ids: Set[Any]):
        self.keywords[keyword].source_ids -= source_ids


class KeywordExtractRule(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, parse_result: Any, document_vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, postprocessor: Any) -> List[SpecifiedKeyword]:
        pass


class StopwordRule(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, parse_result: Any, document_vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, postprocessor: Any) -> List[SpecifiedKeyword]:

        pass


class AbstractKeywordExtractor(metaclass=ABCMeta):

    @abstractmethod
    def exec(self, parse_result: Any, document_vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, token_2_vector: Dict[Any, float], specifiable_word_weight: Dict[str, float], postprocessor: Any, mean_center: Any) -> KeywordsType:
        pass
