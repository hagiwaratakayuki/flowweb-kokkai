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
