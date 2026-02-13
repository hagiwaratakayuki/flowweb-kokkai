from collections import deque
import token
from typing import Callable, Dict, Iterable, Tuple, Optional, TypedDict

from spacy.language import Language
import numpy as np


from ..commons.const import MAIN_POS
from ..commons.projections import project_vector


class SentimentBaseDict(TypedDict):
    negative: Iterable[Tuple[np.ndarray, int]]
    positive: Iterable[Tuple[np.ndarray, int]]


class SentimentScoreDict(TypedDict):
    negative: float
    positive: float
    neutral: float


class SpacyBasicSentiment:
    sentiment_vecs: SentimentBaseDict
    cache: Dict[any, SentimentScoreDict]

    def __init__(self, posiwords, negwords, nlp: Language, projecter: project_vector = project_vector, punct=' '):
        self.cache = {}
        self.posiwords = posiwords
        self.negwords = negwords
        self.punct = punct
        pdoc = nlp(self.punct.join(self.posiwords))
        ndoc = nlp(self.punct.join(self.negwords))
        self.sentiment_vecs = {}

        for doc, key in [(pdoc, 'positive',), (ndoc, 'negative')]:

            norms = {
                token.norm_: token.vector for token in doc if token.pos_ not in MAIN_POS}

            projected_dict = projecter(norms)

            self.sentiment_vecs[key] = (
                deque(projected_dict.values()), len(norms),)

    def evaluate(self, norm_to_vectors: Dict[any, np.ndarray]) -> Dict[any, SentimentScoreDict]:

        index2key = {}
        vectors = []
        index = -1

        for key, vector in norm_to_vectors.items():
            if key in self.cache:
                continue
            index += 1
            index2key[index] = key
            vectors.append(vector)
        if index > -1:
            vector_array = np.array(vectors)

            polarity_scores_dict: SentimentBaseDict = {}
            for polarity, pack in self.sentiment_vecs.items():
                polarity_vectors, polarity_vectors_len = pack
                distances = np.sum([np.linalg.norm(vector_array - polarity_vector, axis=1)
                                   for polarity_vector in polarity_vectors], axis=0) / polarity_vectors_len

                distances[distances == 0.0] = 1
                polarity_scores_dict[polarity] = 1 / distances
            adajst = 1 / \
                (polarity_scores_dict['positive'] +
                 polarity_scores_dict['negative'])
            polarity_scores_dict['positive'] *= adajst
            polarity_scores_dict['negative'] *= adajst
            index = -1
            new_scores_dict: Dict[any, SentimentScoreDict] = {}
            for positive, negative in zip(polarity_scores_dict['positive'], polarity_scores_dict['negative']):
                index += 1
                key = index2key[index]
                sentiment_score: SentimentScoreDict = {}
                sentiment_score['positive'] = positive
                sentiment_score['negative'] = negative
                sentiment_score['neutral'] = min(
                    negative, positive) / max(negative, positive)
                new_scores_dict[key] = sentiment_score

            self.cache.update(new_scores_dict)
        return {key: self.cache[key]
                for key in norm_to_vectors.keys()}
