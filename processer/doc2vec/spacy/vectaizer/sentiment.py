from collections import deque
from typing import Dict, Iterable, Optional, TypedDict
from fastapi.background import P
import spacy
import numpy as np

from doc2vec import sentiment
from .const import MAIN_POS
from .projections import project_vector


class SentimentBaseDict(TypedDict):
    negative: Iterable[np.ndarray]
    positive: Iterable[np.ndarray]


class SentimentScoreDict(TypedDict):
    negative: float
    positive: float
    neutral: float


class BasicSentiment:
    sentiment_vecs: SentimentBaseDict
    cache: Dict[any, SentimentScoreDict]

    def __init__(self, posiwords, negwords, name, punct=' '):
        self.cache = {}
        nlp = spacy.load(name=name)
        pdoc = nlp(punct.join(posiwords))
        ndoc = nlp(punct.join(negwords))
        self.sentiment_vecs = {}

        for doc, key in [(pdoc, 'positive',), (ndoc, 'negative')]:

            norms = {}
            for token in doc:
                if token.pos_ not in MAIN_POS:
                    continue

                norms[token.norm_] = token.vector
            projected_dict = project_vector(norms)
            self.sentiment_vecs[key] = deque(projected_dict.values())

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
            for polarity, polarity_vectors in self.sentiment_vecs.items():
                total_distance: Optional[np.ndarray] = None
                for polarity_vector in polarity_vectors:
                    distances = np.linalg.norm(
                        vector_array - polarity_vector, axis=1)
                    if total_distance == None:
                        total_distance = distances
                    else:
                        total_distance += distances
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
