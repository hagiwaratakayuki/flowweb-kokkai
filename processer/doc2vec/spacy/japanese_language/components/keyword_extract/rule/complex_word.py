from ast import Tuple
from collections import defaultdict, deque

from functools import reduce
from tkinter import S
import token
from typing import Dict, Iterator, List, Optional, Set

import numpy as np


from ..stopwords import remove_stopwords
from ..util.inflection_check import is_sahen, is_adverbable, is_tail, is_popular_noun
from doc2vec.spacy.components.keyword_extracter.protocol import KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc, Token

from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction, NounVectors

CONPOUND_TAG = 'compound'
KEEP_TAG = {'compound', 'nmod', 'obl', 'nsubj'}
MAIN_TAG = {'nsubj', 'ROOT'}
EMPTY_SET = set()


class ComplexWordDTO:
    is_force: bool
    tokens: List[Token]
    is_complex_noun: bool
    source_ids: Set

    def get_vector(self, noun_vecter) -> np.ndarray:
        return np.average([noun_vecter[token.norm] for token in self.tokens], axis=0)


class ComplexWordExtractRule(KeywordExtractRule):
    def execute(self, doc: Doc, vector, sentiment_results, dto, tokenid2keyword: TokenID2Keyword, projecter: ProjectFunction):
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
                    if token.tag_ in KEEP_TAG:
                        canditate_tokens.append(token)
                    else:
                        is_canditate_exists = False
                        if is_canditate_exists == True:
                            complex_word_tokens, noun_vectors = self._update_section(canditate_tokens=canditate_tokens,
                                                                                     complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)

                        canditate_tokens = []

                elif token.tag_ == CONPOUND_TAG:
                    is_canditate_exists = True
        if is_canditate_exists == True:
            complex_word_tokens, noun_vectors = self._update_section(canditate_tokens=canditate_tokens,
                                                                     complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)
        sks = []
        removes = defaultdict(set)
        for complex_word, data in complex_word_tokens.items():
            sk = SpecifiedKeyword(
                headword=complex_word,
                vector=data.get_vector(),
                is_force=data.is_force,
                source_ids=data.source_ids
            )

            for source_id in sk.source_ids:

                for target_sk in tokenid2keyword.get(source_id, {}).values():
                    target_sk.source_ids -= source_id

            tokenid2keyword[source_id][sk.id] = sk

        return tokenid2keyword

    def _update_section(self, canditate_tokens: List[Token], complex_word_tokens: Dict[str, ComplexWordDTO], noun_vectors: NounVectors):

        is_complex_noun = False
        is_force = False
        for token in canditate_tokens:
            is_complex_noun |= is_popular_noun(token)
            is_force |= token.tag in MAIN_TAG
            if is_complex_noun == True and is_force == True:
                break

        if is_complex_noun == True:
            key = ''
            source_ids = set()

            for token in canditate_tokens:
                noun_vectors[token.norm_] = token.vector
                key += token.orth_
                source_ids.add(token.i)
            data = complex_word_tokens[key]
            data.is_force |= is_force
            data.tokens = canditate_tokens
            data.source_ids = source_ids

        return complex_word_tokens, noun_vectors
