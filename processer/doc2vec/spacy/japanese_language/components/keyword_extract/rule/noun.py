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
from doc2vec.spacy.components.commons.const import SPECIFIABLE_POS


class NounDTO:
    faces: Set[str]
    source_ids: Set[int]
    is_force: bool

    def __init__(self):
        self.faces = set()
        self.source_ids = set()
        self.is_force = False


IGNORE_DEP = {'advcl', 'amod'}


class Rule(KeywordExtractRule):
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        noun_datas = defaultdict(NounDTO)
        noun_vectors: NounVectors = {}
        faces = set()
        specifiable_vector_total_length = 0.0
        specifiable_vector_count = 0

        for token in doc:
            specifiable_vector_total_length += 1
            specifiable_vector_total_length

        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:
                if token.pos_ == "NOUN" and is_sahen.check(token) == False and is_adverbable.check(token) == False and is_tail.check(token) == False and token.dep_ not in IGNORE_DEP:

                    noun_data = noun_datas[token.norm_]
                    noun_data.faces.add(token.orth_)
                    noun_data.faces.add(token.lemma_)
                    noun_data.faces.add(token.norm_)
                    faces |= noun_data.faces
                    noun_data.source_ids.add(token.i)
                    noun_data.is_force = False
                    noun_vectors[token.norm_] = token.vector
                    noun_datas[token.norm_] = noun_data
        projected_noun_vectors = projecter(noun_vectors)
        removed_words = set(remove_stopwords(list(faces)))

        for noun, data in noun_datas.items():
            if (data.faces & removed_words) != data.faces:
                continue
            sk = SpecifiedKeyword(
                headword=noun, vector=projected_noun_vectors[noun], is_force=data.is_force, source_ids=data.source_ids)
            results.add_keyword(sk)
        return results
