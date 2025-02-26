from collections import deque
import math
import token
from typing import Dict, Iterable, List, TypedDict
from xml.dom.expatbuilder import theDOMImplementation
import spacy
from spacy.tokens import Doc, Token
import numpy as np

from data_loader.dto import DTO

from .const import MAIN_DEP, MAIN_POS
from processer.doc2vec.spacy.vectaizer.projections import project_vector


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

    def __init__(self, poswords: List[str], negwords: List[str], name, punct=' '):
        pass

    def exec(self, doc: Doc, data: DTO):
        tokens = deque()
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

        projected_vecter_dict = project_vector(norm_to_vecter)

        sentiment_vectors = {
            token.norm_: projected_vecter_dict[token.norm_] for token in doc if token.pos_ in MAIN_POS}

    def calicurate_sentiment(self, sentiment_vectors: Dict[any, np.ndarray]):
