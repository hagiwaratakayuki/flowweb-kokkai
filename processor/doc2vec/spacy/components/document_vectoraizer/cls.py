from collections import defaultdict, deque
import math


from typing import Any, Callable, Deque, Dict, List, Optional, Tuple


import numpy as np
from spacy.tokens import Doc, Token, Span


from data_loader.dto import DTO

from doc2vec.base.protocol.sentiment import SentimentResult, SentimentVectors, SentimentWeights
from doc2vec.spacy.components.commons.projections import project_vector
from doc2vec.base.document_vectoraizer.protocol import AbstractDocumentVectoraizer
from ..sentiment.cls import SpacyBasicSentiment

from ..commons.const import MAIN_DEP, MAIN_POS, SPECIFIABLE_POS


class SpacyBasicDocumentVectoraizer(AbstractDocumentVectoraizer):

    def initialize(self, sentiment_analaizer: SpacyBasicSentiment, projecter: project_vector = project_vector):
        self.sentiment = sentiment_analaizer
        self.projecter = projecter

    def exec(self, doc: Doc, data: DTO):

        sent_count = len(list(doc.sents))
        if sent_count == 0:

            return None, None, None, data

        specifiable_tokens = set()

        token_to_vector = {token.norm_: token.vector for token in doc}

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
        if specifiable_tokens_distance_std != 0:
            weights = 1 - (np.tanh(2 * (specifiable_tokens_distance -
                                        specifiable_tokens_distance_avg) / specifiable_tokens_distance_std) + 1) / 2
        else:
            weights = (specifiable_tokens_distance -
                       specifiable_tokens_distance / 2) / 2
        # 0.1 to 1.0
        weights *= 1.8
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

        sent_number = -1
        total_score = 0.0
        scored_sents: Deque[Deque[Tuple[Token, float]]] = deque()

        for sent in doc.sents:
            sent_number += 1
            scored_sent, sentence_total_score = self._get_sentence_score(
                sent=sent, sent_weight=sent_to_weights[sent_number] / all_sent_weight, specifiable_token_to_weight=specifiable_token_to_weight)
            scored_sents.append(scored_sent)
            total_score += sentence_total_score

        main_pos_to_vecters = {
            token.norm_: projected_vecter_dict[token.norm_] for token in doc if token.pos_ in MAIN_POS}
        sentiment_scores = self.sentiment.evaluate(main_pos_to_vecters)

        scored_vectors_deque = deque()
        token_to_score = {}
        for scored_sent in scored_sents:
            for token, score in scored_sent:
                reguraized_score = score / total_score
                token_vector = projected_vecter_dict[token.norm_] * \
                    reguraized_score
                token_to_score[token] = reguraized_score

                scored_vectors_deque.append(token_vector)
        scored_vectors = np.vstack(scored_vectors_deque).T
        document_vector = np.sum(scored_vectors.T, axis=0)

        default_score = {"positive": 0.5, "negative": 0.5, "neutral": 0.5}
        sentiment_vectors = SentimentVectors()
        sentiment_weights = SentimentWeights()
        sentiment_result = SentimentResult()
        polarity_scores = {}
        total_polarty_score = 0.0
        for polarity in ["positive", "negative", "neutral"]:
            polarity_sentiment_scores = deque()
            polarity_score = 0.0
            for scored_sent in scored_sents:
                for token, score in scored_sent:
                    sentiment_score = score * \
                        sentiment_scores.get(token.norm_, default_score)[
                            polarity]
                    polarity_sentiment_scores.append(sentiment_score)
                    polarity_score += sentiment_score
            sentiment_vector = np.sum(
                (scored_vectors * polarity_sentiment_scores).T / (polarity_score or 1.0), axis=0)
            setattr(sentiment_vectors, polarity, sentiment_vector)
            polarity_scores[polarity] = polarity_score
            if polarity != "neutral":
                total_polarty_score += polarity_score
        negaposi_score = []
        for polarity, polarity_score in polarity_scores.items():
            if polarity != "neutral":
                weight = polarity_score / total_polarty_score
                setattr(sentiment_weights, polarity, weight)
                negaposi_score.append(weight)
        sentiment_weights.neutral = min(negaposi_score) / max(negaposi_score)
        sentiment_result.weights = sentiment_weights
        sentiment_result.vectors = sentiment_vectors
        return document_vector, sentiment_result, token_to_score

    def _get_sentence_score(self, sent: Span, specifiable_token_to_weight: Dict[Any, float], sent_weight: float):
        total_step_count = 0.0
        token_steps = deque()
        last_step_count = 0.0
        for token in sent:
            step_count = specifiable_token_to_weight.get(token.norm_, 0.1)
            total_step_count += step_count
            token_steps.append((token, step_count, ))
            last_step_count = step_count
        total_step_count -= last_step_count
        total_step_count = total_step_count or 1.0
        position = 0.0
        result = deque()
        total_score = 0.0
        for token, step_count in token_steps:

            score = 1 - math.sin(math.pi * position / total_step_count) * \
                0.8 - 0.1 * position / total_step_count
            score *= step_count * sent_weight

            total_score += score
            position += step_count
            result.append((token, score, ))

        return result, score
