
from collections import defaultdict, deque
import math

from spacy.tokens import Doc
from typing import Any, Deque, Iterable, Optional, Dict, Tuple

import numpy as np
from scipy import special
from doc2vec.base.protocol.vectorizer import WordVectorizer, WordToVecDictType
from doc2vec.base.protocol.sentiment import SentimentAnarizer, SentimentResult, SentimentVectors, SentimentWeights
from data_loader.dto import DTO
from doc2vec.base.protocol.tokenizer import TokenDTO

from doc2vec.base.protocol.postprocessor import ExecResponseType, PostprocessorBase
from doc2vec.base.protocol.keyword_extractor import AbstractKeywordExtractor


class Postproceesor(PostprocessorBase):
    def __init__(self, vectorizer: WordVectorizer, sentiment_anarizer: SentimentAnarizer, keyword_extractor: AbstractKeywordExtractor):
        self.sentiment_anaraizer = sentiment_anarizer
        self.vectorizer = vectorizer
        self.keyword_extractor = keyword_extractor

    def exec(self, parse_result: Doc, data: DTO) -> ExecResponseType:
        reguraized_forms = parse_result.get_reguraized_forms()

        if not reguraized_forms:

            return None, None, None, data

        meanable_tokens = set()

        word_to_vector, word_to_vector_length = self.vectorizer.get_vectors(
            reguraized_forms)

        meanable_tokens_vector_list = []
        meanable_tokens_vector_length_list = []
        index2reg = {}
        index = -1
        sent_number = -1
        sents_to_specifi_tokens = defaultdict(set)
        total_vector_length = 0.0

        main_pos_to_vectors = {}
        for sent in parse_result.get_sents():
            sent_number += 1
            sent_to_specifi_tokens = sents_to_specifi_tokens[sent_number]

            for token in sent:
                if not self._check_meanable_pos(token):
                    continue
                token_reguraized = self._get_reguraized(token)
                token_vector = word_to_vector[token_reguraized]
                if token_vector is None:
                    continue

                if (token_reguraized not in meanable_tokens):

                    index += 1
                    token_vector_length = word_to_vector_length[token_reguraized]
                    meanable_tokens_vector_list.append(token_vector)

                    meanable_tokens_vector_length_list.append(
                        token_vector_length)

                    index2reg[index] = token_reguraized
                    meanable_tokens.add(token_reguraized)
                    sent_to_specifi_tokens.add(token_reguraized)
                    main_pos_to_vectors[token_reguraized] = word_to_vector[token_reguraized]
                    total_vector_length += token_vector_length

        if index == -1:
            return None, None, None, data

        meanable_tokens_vector_array = np.array(meanable_tokens_vector_list)

        length_emphasies = np.divide(
            meanable_tokens_vector_length_list, total_vector_length / float(index))

        emphasized_vector = np.einsum('ij,i->ij',
                                      meanable_tokens_vector_array, length_emphasies)
        emphasized_mean_center = np.average(
            meanable_tokens_vector_array, axis=0)
        mean_diff_vectors = emphasized_vector - emphasized_mean_center
        raw_mean_diff_lengths = np.linalg.norm(mean_diff_vectors, axis=1)
        reverse_weights = raw_mean_diff_lengths / \
            np.average(raw_mean_diff_lengths)

        sent_count = sent_number + 1

        index = -1
        mean_word_weight = {}
        min_weight = float('inf')
        for reverce_weight in reverse_weights:
            index += 1
            if reverce_weight == 0.0:
                weight = 0.0
            else:
                weight = 1 / reverce_weight
            mean_word_weight[index2reg[index]] = weight
            if min_weight > weight:
                min_weight = weight

        all_sent_weight = 0.0
        sent_weights = []
        index = 0

        while index < sent_count:

            sent_to_specifi_tokens = sents_to_specifi_tokens[index]

            index += 1

            sent_total_weight = 0.0

            for reguraized in sent_to_specifi_tokens:
                sent_total_weight += mean_word_weight[reguraized]

            sent_weights.append(sent_total_weight)
            all_sent_weight += sent_total_weight

        sent_number = -1
        total_score = 0.0
        scored_sents: Deque[Deque[Tuple[Any, float]]] = deque()
        sent_to_weights = np.exp(
            np.divide(sent_weights, all_sent_weight / float(sent_count)))

        for sent in parse_result.get_sents():

            sent_number += 1
            scored_sent, sentence_total_score = self._get_sentence_score(
                sent=sent, sent_weight=sent_to_weights[sent_number], meanable_token_to_weight=mean_word_weight, min_step_count=min_weight)
            scored_sents.append(scored_sent)
            total_score += sentence_total_score

        sentiment_scores = self.sentiment_anaraizer.execute(
            main_pos_to_vectors)

        scored_vectors_deque = deque()

        token_2_vector = {}

        for scored_sent in scored_sents:
            for token, score in scored_sent:

                reguraized_score = score / total_score

                token_vector = self._get_vector(
                    word_to_vector=word_to_vector, token=token)

                if token_vector is None:
                    token_vector = self._get_zero_array()

                token_vector *= reguraized_score

                token_2_vector[token] = token_vector

                scored_vectors_deque.append(token_vector)

        scored_vectors = np.array(scored_vectors_deque)
        document_vector = np.sum(scored_vectors, axis=0)

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
                np.einsum('ij,i->ij', scored_vectors, polarity_sentiment_scores) / (polarity_score or 1.0), axis=0)
            setattr(sentiment_vectors, polarity, sentiment_vector)
            polarity_scores[polarity] = polarity_score
            if polarity != "neutral":
                total_polarty_score += polarity_score
        negaposi_score = []
        for polarity, polarity_score in polarity_scores.items():
            if polarity != "neutral":
                reverce_weight = polarity_score / total_polarty_score
                setattr(sentiment_weights, polarity, reverce_weight)
                negaposi_score.append(reverce_weight)
        sentiment_weights.neutral = min(negaposi_score) / max(negaposi_score)
        sentiment_results.weights = sentiment_weights
        sentiment_results.vectors = sentiment_vectors

        keywords = self.keyword_extractor.exec(
            parse_result=parse_result, document_vector=document_vector, sentiment_results=sentiment_results, dto=data, token_2_vector=token_2_vector, postprocessor=self, mean_center=emphasized_mean_center)
        return document_vector, sentiment_results, keywords, data

    def _get_mean_center(self, parse_result: Doc):

        for token in parse_result:
            token.norm

    def _get_sentence_score(self, sent: Iterable[Any], meanable_token_to_weight: Dict[Any, float], sent_weight: float, min_step_count: float):
        total_step_count = 0.0
        token_steps = deque()
        last_step_count = 0.0
        now_step_count = 0.0
        for token in sent:
            step_count = meanable_token_to_weight.get(
                self._get_reguraized(token), min_step_count * 0.1)
            total_step_count += step_count
            token_steps.append((token, now_step_count, ))
            last_step_count = step_count
            now_step_count += step_count
        total_step_count -= last_step_count
        total_step_count = total_step_count or 1.0
        position = 0.0
        result = deque()
        total_score = 0.0
        for token, step_count in token_steps:
            adjasted_position = step_count / total_step_count
            score = 1 - math.sin(math.pi * adjasted_position) * \
                0.2 - 0.9 * adjasted_position
            score *= sent_weight

            total_score += score
            position += step_count
            result.append((token, score, ))

        return result, total_score

    def _check_meanable_pos(self, token) -> bool:
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
