from spacy.tokens import Doc
import numpy as np

from doc2vec.protocol.sentiment import SentimentResult
from data_loader.dto import DTO


class BasicKeywordExtratcer:
    def exec(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO):
        pass
