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

    def add_keyword(self, keyword: SpecifiedKeyword, tokens: Iterable[Token], is_overwrite_token=True):
        self.keywords.append(keyword)
        if is_overwrite_token == True:

            for token in tokens:
                self.token_id_2_keyword[token.i][keyword.id].source_ids -= token.i
                self.token_id_2_keyword[token.i][keyword.id] = keyword
        else:
            for token in tokens:
                self.token_id_2_keyword[token.i][keyword.id] = keyword
        self.keywords.append(keyword)

    def get_keywords(self):
        # refaernce shortcut
        return [keyword for keyword in self.keywords if keyword.source_ids != EMPTY_SET]


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        pass
