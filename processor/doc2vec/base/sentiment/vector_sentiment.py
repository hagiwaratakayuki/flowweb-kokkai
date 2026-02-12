from collections import deque
from typing import Deque, Dict, List, Tuple

import numpy as np
from doc2vec.base.protocol.sentiment import SentimentAnarizer
from doc2vec.base.protocol.vectorizer import WordVectorizer
from doc2vec.spacy.components.sentiment.cls import SentimentBaseDict, SentimentScoreDict


class VectorSentiment(SentimentAnarizer):
    _posi_vectors: List[np.ndarray]
    _nega_vectors: List[np.ndarray]
    cache: Dict
    sentiment_vecs: Dict[str, Tuple[Deque[np.ndarray], int]]

    def __init__(self, posi_words: List[str], nega_words: List[str], vectorizer: WordVectorizer):
        self.sentiment_vecs = {}
        self.cache = {}
        for words, key in [(posi_words, 'positive',), (nega_words, 'negative')]:

            vectors_lengths = vectorizer.get_vectors(words)

            self.sentiment_vecs[key] = (
                deque(vectors_lengths[0].values()), len(words),)

    def execute(self, words: Dict[str, np.ndarray]) -> Dict[str, SentimentScoreDict]:

        index2key = {}
        vectors = []
        index = -1

        for key, vector in words.items():
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
                for key in words.keys()}
