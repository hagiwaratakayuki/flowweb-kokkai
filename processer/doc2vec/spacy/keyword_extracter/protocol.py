from typing import Dict, List
from spacy.tokens import Doc
import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword

type NounMap = List[Dict[str, List[int]]]


class KeywordExtractRule:
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: List[SpecifiedKeyword], nounmap: NounMap) -> List[SpecifiedKeyword]:

        pass
