import numpy as np
import random

from doc2vec.base.protocol.sentiment import SentimentWeights
from doc2vec.base.protocol.sentiment import SentimentVectors
from doc2vec.base.protocol.sentiment import SentimentResult


def build_mock_sentiment_result(d1: int):
    neutral = random.random()
    positive = random.random()
    negative = random.random()
    total = sum([neutral, positive, negative])
    weights = SentimentWeights()
    weights.neutral = neutral / total
    weights.positive = positive / total
    weights.negative = negative / total
    neutral = np.random.rand(d1)
    positive = np.random.rand(d1)
    negative = np.random.rand(d1)
    vectors = SentimentVectors()

    vectors.neutral = neutral
    vectors.positive = positive
    vectors.negative = negative
    result = SentimentResult()
    result.vectors = vectors
    result.weights = weights
    return result
