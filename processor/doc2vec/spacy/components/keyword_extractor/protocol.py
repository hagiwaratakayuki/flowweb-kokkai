from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Optional, Set, Union
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.protocol import SpacySpecifiedKeyword as SpacySpecifiedKeywordType
from doc2vec.base.protocol.postprocessor import DocVectorType


type Token2Keyword = Dict[Token, Set[SpacySpecifiedKeywordType]]


EMPTY_SET = set()


class ExtractResultDTO:
    token_2_keyword: Token2Keyword
    keywords: Set[SpacySpecifiedKeywordType]

    def __init__(self):
        self.token_2_keyword = defaultdict(set)
        self.keywords = set()

    def add_keyword(self, keyword: SpacySpecifiedKeywordType, is_overwrite_token=True):

        self.keywords.add(keyword)
        if is_overwrite_token == True:

            for target_keyword in self.get_by_source_ids(keyword.tokens):

                target_keyword.tokens -= keyword.tokens

        for source_id in keyword.tokens:
            self.token_2_keyword[source_id].add(keyword)

    def remove_kewywords(self, source_ids):

        for kw in self.get_by_source_ids(source_ids=source_ids):

            kw.tokens -= source_ids

    def get_keywords(self):
        # refarence shortcut
        return [keyword for keyword in self.keywords if keyword.tokens != EMPTY_SET]

    def get_by_source_ids(self, source_ids: Iterable[Any]) -> Set[SpacySpecifiedKeywordType]:
        ret: Set[SpacySpecifiedKeywordType] = set()
        for source_id in source_ids:
            ret.update(self.token_2_keyword.get(source_id, []))
        return ret

    def check_by_source_ids(self, source_ids):
        return {source_id for source_id in source_ids if source_id in self.token_2_keyword}

    def substruct_sorce_id(self, keyword: SpacySpecifiedKeywordType, source_ids: Set[Any]):
        self.keywords[keyword].source_ids -= source_ids


class KeywordExtractRule:
    def execute(self, parse_results: Any, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, token_2_score: Dict[Any, float], postprocessor: Any, results: ExtractResultDTO, model_name: str) -> List[SpacySpecifiedKeywordType]:
        pass
