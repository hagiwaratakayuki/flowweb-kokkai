from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Callable, Dict, FrozenSet, Iterable, List, Optional, Set, Union
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction

type TokenID2Keyword = Dict[Any, Set[SpecifiedKeyword]]


EMPTY_SET = set()


class ExtractResultDTO:
    token_id_2_keyword: TokenID2Keyword
    keywords: Set[Any, SpecifiedKeyword]

    def __init__(self):
        self.token_id_2_keyword = defaultdict(set)
        self.keywords = set()

    def add_keyword(self, keyword: SpecifiedKeyword, is_overwrite_token=True):
        self.keywords.add(keyword)
        if is_overwrite_token == True:

            for target_keyword in self.get_by_source_ids(keyword.source_ids):

                target_keyword.source_ids -= keyword.source_ids
            self.token_id_2_keyword[source_id].add(keyword)
        else:
            for source_id in keyword.source_ids:
                self.token_id_2_keyword[source_id].add(keyword)

    def get_keywords(self):
        # refarence shortcut
        return [keyword for keyword in self.keywords if keyword.source_ids != EMPTY_SET]

    def get_by_source_ids(self, source_ids: Iterable[Any]) -> Set[SpecifiedKeyword]:
        ret: Set[SpecifiedKeyword] = set()
        for source_id in source_ids:
            ret.update(self.token_id_2_keyword.get(source_id, []))
        return ret

    def check_by_source_ids(self, source_ids):
        return {source_id for source_id in source_ids if source_id in self.token_id_2_keyword}

    def substruct_sorce_id(self, keyword: SpecifiedKeyword, source_ids: Set[Any]):
        self.keywords[keyword].source_ids -= source_ids


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        pass
