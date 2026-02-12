from abc import ABCMeta, abstractmethod
from typing import Any

import numpy as np

from processor.doc2vec.base.protocol.sentiment import SentimentResult


class AbstractPipelineKeywordExtractor(metaclass=ABCMeta):
    @abstractmethod
    def exec(self, parse_result: Any, document_vectorDoc, vector: np.ndarray, sentiment_results: SentimentResult, dto: Any, token_2_score: Any):
        pass
