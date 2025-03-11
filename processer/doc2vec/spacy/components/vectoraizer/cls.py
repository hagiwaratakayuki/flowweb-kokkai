from collections import defaultdict, deque
import math

import token
from typing import Callable, Deque, List, Optional, Tuple


import numpy as np
from spacy.tokens import Doc, Token


from data_loader.dto import DTO

from doc2vec.protocol.sentiment import SentimentResult, SentimentVectors, SentimentWeights
from ..sentiment.cls import BasicSentiment

from ..commons.const import MAIN_DEP, MAIN_POS, SPECIFIABLE_POS


class WeightCalicurater:
    def __init__(self, total):
        self.position = 0.0
        self.total = float(total)

    def get_score(self):
        ret = 1 - math.sin(math.pi * self.position /
                           self.total) * 0.8 - 0.1 * self.position / self.total
        self.position += 1.0
        return ret


class TokenWeightCaliculater(WeightCalicurater):
    def get_score(self, token: Token):
        adjast = 1.0
        if token.dep_ in MAIN_DEP:
            adjast = 1.5
        elif token.pos_ not in MAIN_POS:
            adjast = 0.5
        ret = super().get_score() * adjast

        return ret


class BasicVectoraizer:

    def initialize(self, sentiment: BasicSentiment, projecter: Callable, token_weight_rules=[]):
        self.sentiment = sentiment
        self.projecter = projecter
        self.token_weight_rules = token_weight_rules

    def exec(self, doc: Doc, data: DTO):
        tokens: Deque[Tuple[Token, float]] = deque()
        sent_count = len(list(doc.sents))
        if sent_count == 0:

            return None, None, None, data
        line_weight_calicurater = self._get_line_weight_claicurater(
            sent_count=sent_count)

        specifiable_tokens = set()

        token_to_vector = {token.norm_ for tokns in doc}

        projected_vecter_dict = self.projecter(token_to_vector)
        specifiable_tokens_vector_list = []
        index2norm = {}
        index = -1
        sent_number = -1
        sents_to_specifi_tokens = defaultdict(set)
        sents_to_tokens = defaultdict(set)
        for sent in doc.sents:
            sent_number += 1
            sent_to_specifi_tokens = sents_to_specifi_tokens[sent_number]
            sent_to_tokens = sents_to_tokens[sent_number]
            for token in doc:

                if (token.vector_norm == 0) or (token.pos_ not in SPECIFIABLE_POS):
                    continue
                if (token.norm_ not in specifiable_tokens):
                    index += 1
                    specifiable_tokens_vector_list.append(
                        projected_vecter_dict[token.norm_])
                    index2norm[index] = token.norm_
                specifiable_tokens.add(token.norm_)
                sent_to_specifi_tokens.add(token.norm_)
                sent_to_tokens.add(token.norm_)

        specifiable_token_vector = np.array(specifiable_tokens_vector_list)
        specifiable_tokens_center = np.average(
            specifiable_token_vector, axis=0)
        specifiable_tokens_distance = np.linalg.norm(
            specifiable_token_vector - specifiable_tokens_center, axis=1)
        specifiable_tokens_distance_avg = np.average(
            specifiable_tokens_distance)
        specifiable_tokens_distance_std = np.std(specifiable_tokens_distance)

        # sigmoid function,  avg - std to avge + std →　0 to 1, (tanh(ax/2) +1) / 2,  a = 4
        weights = 1 - (np.tanh(2 * (specifiable_tokens_distance -
                                    specifiable_tokens_distance_avg) / specifiable_tokens_distance_std) + 1) / 2
        # 0.1 to 1.0
        weights *= 0.9
        weights += 0.1
        index = -1
        specifiable_token_to_weight = {}
        for weight in weights:
            index += 1
            specifiable_token_to_weight[index2norm[index]] = weight

        for sent in doc.sents:
            token_score_caliculater = self(len(sent))
            line_score = line_weight_calicurater.get_score()

            scored_subnodes = [
                (token, line_score * token_score_caliculater.get_score(token=token),) for token in sent]
            tokens.extend(scored_subnodes)

        norm_to_vecters = {
            token.norm_: projected_vecter_dict[token.norm_] for token in doc if token.pos_ in MAIN_POS}
        sentiment_scores = self.sentiment.evaluate(norm_to_vecters)
        total_score = sum([r[1] for r in tokens])
        document_vector = sum(
            [projected_vecter_dict[token.norm_] * score for token, score in tokens]) / total_score

        default_score = {"positive": 0.5, "negative": 0.5, "neutral": 0.5}
        sentiment_vectors = SentimentVectors()
        sentiment_weights = SentimentWeights()
        sentiment_result = SentimentResult()

        for polarity in ["positive", "negative", "neutral"]:
            weighted_tokens: List[Tuple[Token, float]] = [
                (token, score * sentiment_scores.get(token.norm_, default_score)[polarity],) for token, score in tokens]
            total_sentimented_score = sum([r[1] for r in weighted_tokens])
            sentiment_vector = sum(
                [token.vector * score for token, score in weighted_tokens]) / total_sentimented_score
            sentimemnt_weight = total_sentimented_score / total_score
            setattr(sentiment_vectors, polarity, sentiment_vector)
            setattr(sentiment_weights, polarity, sentimemnt_weight)
        sentiment_result.weights = sentiment_weights
        sentiment_result.vectors = sentiment_vectors
        return document_vector, sentiment_result

    def _get_line_weight_claicurater(self, sent_count):
        return WeightCalicurater(sent_count)
