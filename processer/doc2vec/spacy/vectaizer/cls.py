from collections import deque
import math
import token
from typing import Deque, Dict, Iterable, List, Tuple, TypedDict
from xml.dom.expatbuilder import theDOMImplementation
import spacy
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO

from doc2vec.protocol.sentiment import SentimentResult, SentimentVectors, SentimentWeights
from .sentiment import Sentiment

from .const import MAIN_DEP, MAIN_POS
from .projections import project_vector


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


class BasicVectaizer:

    def __init__(self, sentiment: Sentiment, projecter=project_vector):
        self.sentiment = sentiment
        self.projecter = projecter

    def exec(self, doc: Doc, data: DTO):
        tokens: Deque[Tuple[Token, float]] = deque()
        sent_count = len(doc.sents)
        if sent_count == 0:

            return None, None, None, data
        line_score_calicurater = WeightCalicurater(sent_count)
        for sent in doc.sents:
            token_score_caliculater = TokenWeightCaliculater(len(sent))
            line_score = line_score_calicurater.get_score()

            scored_subnodes = [
                (token, line_score * token_score_caliculater.get_score(token=token),) for token in sent]
            tokens.extend(scored_subnodes)
        norm_to_vecter = {token.norm_: token.vector for token in doc}

        projected_vecter_dict = self.projecter(norm_to_vecter)

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
