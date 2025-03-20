
from collections import defaultdict, deque


from typing import Dict, Iterator, List, Optional, Set

import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult


from ..util.tag_check import is_sahen, is_adverbable, is_tail, is_popular_noun
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc, Token

from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction, NounVectors

CONPOUND_DEP = 'compound'
KEEP_DEP = {'compound', 'nmod', 'obl', 'obj', 'nsubj', 'ROOT'}
MAIN_DEP = {'nsubj', 'ROOT'}
EMPTY_SET = set()


class ComplexWordDTO:
    is_force: bool
    tokens: List[Token]
    is_complex_noun: bool
    source_ids: Set

    def __init__(self):
        self.is_force = False
        self.tokens = []
        self.is_complex_noun = False
        self.source_ids = set()

    def get_vector(self, complessed_noun_vectors) -> np.ndarray:

        return np.average([complessed_noun_vectors[token.norm_] for token in self.tokens], axis=0)


class Rule(KeywordExtractRule):
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:
        complex_word_tokens: Dict[str,
                                  ComplexWordDTO] = defaultdict(ComplexWordDTO)
        noun_vectors: NounVectors = {}

        for noun_chunk in doc.noun_chunks:

            if len(noun_chunk) == 1:

                continue

            is_canditate_exists = False
            canditate_tokens: List[Token] = []
            for token in noun_chunk:

                if is_canditate_exists == True:

                    if token.dep_ in KEEP_DEP:
                        canditate_tokens.append(token)

                    else:

                        is_canditate_exists = False

                        complex_word_tokens, noun_vectors = self._update_section(canditate_tokens=canditate_tokens,
                                                                                 complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)

                        canditate_tokens = []

                elif token.dep_ == CONPOUND_DEP:
                    is_canditate_exists = True

                    canditate_tokens.append(token)
            if is_canditate_exists == True:
                complex_word_tokens, noun_vectors = self._update_section(canditate_tokens=canditate_tokens,
                                                                         complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)
        complessed_noun_vectors = projecter(noun_vectors)
        for complex_word, data in complex_word_tokens.items():

            sk = SpecifiedKeyword(
                headword=complex_word,
                vector=data.get_vector(
                    complessed_noun_vectors=complessed_noun_vectors),
                is_force=data.is_force,
                source_ids=data.source_ids
            )
            results.add_keyword(sk)

        return results

    def _update_section(self, canditate_tokens: List[Token], complex_word_tokens: Dict[str, ComplexWordDTO], noun_vectors: NounVectors):
        if len(canditate_tokens) <= 1:
            return complex_word_tokens, noun_vectors

        is_complex_noun = False
        is_force = False
        for token in canditate_tokens:
            is_complex_noun |= is_popular_noun.check(token)
            is_force |= token.dep_ in MAIN_DEP
            if is_complex_noun == True and is_force == True:
                break

        if is_complex_noun == True:
            key = ''
            source_ids = set()

            for token in canditate_tokens:
                noun_vectors[token.norm_] = token.vector
                key += token.norm_
                source_ids.add(token)

            data = complex_word_tokens[key]
            data.is_force |= is_force
            data.tokens = canditate_tokens
            data.source_ids |= source_ids

        return complex_word_tokens, noun_vectors
