from collections import defaultdict, deque
import math


from turtle import position
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple


import numpy as np
from spacy.tokens import Doc, Token, Span


from data_loader.dto import DTO

from doc2vec.protocol.sentiment import SentimentResult, SentimentVectors, SentimentWeights
from ..sentiment.cls import BasicSentiment

from ..commons.const import MAIN_DEP, MAIN_POS, SPECIFIABLE_POS


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

        for sent in doc.sents:
            sent_number += 1
            sent_to_specifi_tokens = sents_to_specifi_tokens[sent_number]

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
        sent_to_weights = {}
        all_sent_weight = 0.0

        for sent_number, sent_to_specifi_tokens in sents_to_specifi_tokens.items():
            sent_total_weight = 0.0
            count = 0.0
            sent_count += 1
            for norm in sent_to_specifi_tokens:
                count += 1.0
                sent_total_weight += specifiable_token_to_weight[norm]
            sent_weight = sent_total_weight / count
            sent_to_weights[sent_number] = sent_weight
            all_sent_weight += sent_weight
        all_sent_weight = all_sent_weight or 1.0

        for sent_number in sent_to_weights.keys():
            sent_to_weights[sent_number] /= all_sent_weight
        sent_number = -1
        for sent in doc.sents:
            token_score_caliculater = self(len(sent))
            sent_number += 1

            sent_weight = sent_to_weights[sent_number]

            scored_subnodes = [
                (token, sent_weight * token_score_caliculater.get_score(token=token),) for token in sent]
            tokens.extend(scored_subnodes)

        main_pos_to_vecters = {
            token.norm_: projected_vecter_dict[token.norm_] for token in doc if token.pos_ in MAIN_POS}
        sentiment_scores = self.sentiment.evaluate(main_pos_to_vecters)
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

    def get_token_score(self, sent: Span, specifiable_token_to_weight: Dict[Any, float], sent_weight: float):
        total_step_count = 0.0
        token_steps = deque()
        last_step_count = 0.0
        for token in sent:
            step_count = specifiable_token_to_weight.get(token.norm_, 0.1)
            total_step_count += step_count
            token_steps.append((token, step_count, ))
            last_step_count = step_count
        total_step_count -= last_step_count
        position = 0.0
        result = deque()
        for token, step_count in token_steps:

            score = 1 - math.sin(math.pi * position / total_step_count) * \
                0.8 - 0.1 * position / total_step_count
            score *= step_count
            position += step_count
            result.append((token, score, ))

        return result
