from collections import defaultdict

from typing import Callable, Dict, List, Set

import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult

from ..stopwords import remove_stopwords
from ..util.tag_check import is_sahen, is_adverbable, is_tail
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc

from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction, NounVectors


class NounDTO:
    faces: Set[str]
    source_ids: Set[int]
    is_force: bool

    def __init__(self):
        self.faces = set()
        self.source_ids = set()
        self.is_force = False


IGNORE_TAG = {'compound', 'nmod', 'obl'}
MAIN_TAG = {'nsubj', 'ROOT'}


class Rule(KeywordExtractRule):
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        noun_datas = defaultdict(NounDTO)
        noun_vectors: NounVectors = {}
        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:
                if token.pos_ == "NOUN" and is_sahen.check(token) == False and is_adverbable.check(token) == False and is_tail.check(token) == False and token.tag_ not in IGNORE_TAG:
                    if token.i > 0:
                        if doc[token.i - 1].tag_ in IGNORE_TAG:
                            continue

                    noun_data = noun_datas[token.norm_]
                    noun_data.faces.add(token.orth_)
                    noun_data.source_ids.add(token.i)
                    noun_data.is_force |= token.tag_ in MAIN_TAG
                    noun_vectors[token.norm_] = token.vector
                    noun_datas[token.norm_] = noun_data
        projected_noun_vectors = projecter(noun_vectors)
        noun_datas = {noun: noun_datas[noun]
                      for noun in remove_stopwords(noun_datas.keys())}
        for noun, data in noun_datas.items():
            sk = SpecifiedKeyword(
                headword=noun, vector=projected_noun_vectors[noun], target_words=data.faces, is_force=data.is_force, source_ids=data.source_ids)
            results.add_keyword(sk)
        return results
