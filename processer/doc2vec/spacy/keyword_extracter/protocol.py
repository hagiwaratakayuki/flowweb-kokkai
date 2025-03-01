from typing import Dict, FrozenSet, List
from spacy.tokens import Doc
import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword

type TokenID2Keyword = Dict[any, Dict[FrozenSet, SpecifiedKeyword]]


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: List[SpecifiedKeyword], tokenid2keyword: TokenID2Keyword) -> List[SpecifiedKeyword]:

        pass
