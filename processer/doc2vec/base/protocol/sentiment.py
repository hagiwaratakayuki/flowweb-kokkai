from typing import Dict, Iterable, TypedDict, Tuple
import numpy as np


class SentimentWeights:
    neutral: float
    positive: float
    negative: float


class SentimentVectors:
    neutral: np.ndarray
    positive: np.ndarray
    negative: np.ndarray


class SentimentResult:
    vectors: SentimentVectors
    weights: SentimentWeights


class SentimentBaseDict(TypedDict):
    negative: Iterable[Tuple[np.ndarray, int]]
    positive: Iterable[Tuple[np.ndarray, int]]


class SentimentScoreDict(TypedDict):
    negative: float
    positive: float
    neutral: float


class SentimentAnarizer:
    def execute(self, words) -> Dict[str, SentimentWeights]:
        pass
