
from collections import defaultdict, deque
import math
from typing import Any, Deque, Iterable, Optional, Dict, Tuple

import numpy as np
import scipy as sp
from doc2vec.base.protocol.vectorizer import Vectorizer, WordToVecDictType
from doc2vec.base.protocol.sentiment import SentimentAnarizer, SentimentResult, SentimentVectors, SentimentWeights
from data_loader.dto import DTO
from doc2vec.base.protocol.tokenizer import TokenDTO
from doc2vec.spacy.components.commons.const import MAIN_POS, SPECIFIABLE_POS
from doc2vec.base.protocol.indexer import ExecResponseType, IndexerCls
from doc2vec.base.protocol.keyword_extracter import KeywordExtracterClass


class Indexer(IndexerCls):
    def __init__(self, vectorizer: Vectorizer, sentiment_anarizer: SentimentAnarizer, keyword_extracter: KeywordExtracterClass):
        self.sentiment_anaraizer = sentiment_anarizer
        self.vectorizer = vectorizer
        self.keyword_extracter = keyword_extracter

    def exec(self, parse_result: TokenDTO, data: DTO) -> ExecResponseType:
        reguraized_forms = parse_result.get_reguraized_forms()

        if not reguraized_forms:

            return None, None, None, data

        specifiable_tokens = set()

        word_to_vector, word_to_vector_length = self.vectorizer.get_vectors(
            reguraized_forms)

        specifiable_tokens_vector_list = []
        specifiable_tokens_vector_length_list = []
        index2reg = {}
        index = -1
        sent_number = -1
        sents_to_specifi_tokens = defaultdict(set)

        for sent in parse_result.get_sents():
            sent_number += 1
            sent_to_specifi_tokens = sents_to_specifi_tokens[sent_number]

            for token in sent:
                if not self._check_specifiable_pos(token):
                    continue
                token_vector = self._get_vector(
                    word_to_vector=word_to_vector, token=token)
                if token_vector is None:
                    continue
                token_vector_length = self._get_vector_length(
                    word_to_vector_length=word_to_vector_length, token=token)

                token_reguraized = self._get_reguraized(token)

                if (token_reguraized not in specifiable_tokens):
                    index += 1
                    specifiable_tokens_vector_list.append(token_vector)
                    specifiable_tokens_vector_length_list.append(
                        token_vector_length)
                    index2reg[index] = token_reguraized
                specifiable_tokens.add(token_reguraized)
                sent_to_specifi_tokens.add(token_reguraized)

        specifiable_tokens_vector_length_avg_ratio = (specifiable_tokens_vector_length_list /
                                                      np.average(specifiable_tokens_vector_length_list)) ** 2

        specifiable_token_vector = np.einsum(
            "ij,i->ij", np.array(specifiable_tokens_vector_list), specifiable_tokens_vector_length_avg_ratio)

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
            specifiable_token_to_weight[index2reg[index]] = weight
        sent_to_weights = {}
        all_sent_weight = 0.0

        for sent_number, sent_to_specifi_tokens in sents_to_specifi_tokens.items():

            count = 0.0
            sent_total_weight = 0.0

            for norm in sent_to_specifi_tokens:
                count += 1.0
                sent_total_weight += specifiable_token_to_weight[norm]

            sent_weight = sent_total_weight / (count or 1)
            sent_to_weights[sent_number] = sent_weight
            all_sent_weight += sent_weight
        all_sent_weight = all_sent_weight or 1.0

        sent_number = -1
        total_score = 0.0
        scored_sents: Deque[Deque[Tuple[Any, float]]] = deque()

        for sent in parse_result.get_sents():

            sent_number += 1
            scored_sent, sentence_total_score = self._get_sentence_score(
                sent=sent, sent_weight=sent_to_weights[sent_number] / all_sent_weight, specifiable_token_to_weight=specifiable_token_to_weight)
            scored_sents.append(scored_sent)
            total_score += sentence_total_score

        main_pos_to_vecters = {
            self._get_reguraized(token): self._get_vector(word_to_vector=word_to_vector, token=token) for token in parse_result.get_tokens() if self._check_main_pos(token)}
        sentiment_scores = self.sentiment_anaraizer.execute(
            main_pos_to_vecters)

        scored_vectors_deque = deque()
        token_2_score = {}
        for scored_sent in scored_sents:
            for token, score in scored_sent:

                reguraized_score = score / total_score
                token_vector = self._get_vector(
                    word_to_vector=word_to_vector, token=token)
                if token_vector is None:
                    token_vector = self._get_zero_array()
                token_vector *= reguraized_score
                token_2_score[token] = reguraized_score

                scored_vectors_deque.append(token_vector)
        scored_vectors = np.vstack(scored_vectors_deque).T
        document_vector = np.sum(scored_vectors.T, axis=0)

        default_score = {"positive": 0.5, "negative": 0.5, "neutral": 0.5}
        sentiment_vectors = SentimentVectors()
        sentiment_weights = SentimentWeights()
        sentiment_results = SentimentResult()
        polarity_scores = {}
        total_polarty_score = 0.0
        for polarity in ["positive", "negative", "neutral"]:
            polarity_sentiment_scores = deque()
            polarity_score = 0.0
            for scored_sent in scored_sents:
                for token, score in scored_sent:

                    sentiment_score = score * \
                        sentiment_scores.get(self._get_reguraized(token), default_score)[
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
        sentiment_results.weights = sentiment_weights
        sentiment_results.vectors = sentiment_vectors
        keywords = self.keyword_extracter.exec(
            parse_result=parse_result, document_vector=document_vector, sentiment_results=sentiment_results, dto=data, token_2_score=token_2_score, indexer=self)
        return document_vector, sentiment_results, keywords, data

    def _get_sentence_score(self, sent: Iterable[Any], specifiable_token_to_weight: Dict[Any, float], sent_weight: float):
        total_step_count = 0.0
        token_steps = deque()
        last_step_count = 0.0
        for token in sent:
            step_count = specifiable_token_to_weight.get(
                self._get_reguraized(token), 0.1)
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

    def _check_specifiable_pos(self, token) -> bool:
        pass

    def _check_main_pos(self, token) -> bool:
        pass

    def _get_vector(self, word_to_vector: WordToVecDictType, token: Any) -> Optional[np.ndarray]:
        pass

    def _get_vector_length(self, word_to_vector_length: Dict[str, float], token: Any) -> Optional[float]:
        pass

    def _get_reguraized(self, token) -> str:
        pass

    def _get_zero_array(self):
        return np.zeros(2)
