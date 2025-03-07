from collections import defaultdict
import keyword
from typing import Any, Callable, Dict, FrozenSet, Iterable, List
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction

type TokenID2Keyword = Dict[any, Dict[Any, SpecifiedKeyword]]


EMPTY_SET = set()


class ExtractResultDTO:
    token_id_2_keyword: TokenID2Keyword
    keywords: List[SpecifiedKeyword]

    def __init__(self):
        self.token_id_2_keyword = defaultdict(dict)
        self.keywords = []

    def add_keyword(self, keyword: SpecifiedKeyword, is_overwrite_token=True):
        self.keywords.append(keyword)
        if is_overwrite_token == True:

            for source_id in keyword.source_ids:
                source_id_set = {source_id}
                for target_keyword in self.token_id_2_keyword.get(source_id, {}).values():

                    target_keyword.source_ids -= source_id_set
                self.token_id_2_keyword[source_id][keyword.id] = keyword
        else:
            for source_id in keyword.source_ids:
                self.token_id_2_keyword[source_id][keyword.id] = keyword

    def get_keywords(self):
        # refaernce shortcut
        return [keyword for keyword in self.keywords if keyword.source_ids != EMPTY_SET]

    def remove_keyword(self, keyword: SpecifiedKeyword):
        for source_id in keyword.source_ids:
            self.token_id_2_keyword[source_id][keyword.id].source_ids -= source_id


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        pass
