
from collections import defaultdict, deque


import re
from typing import DefaultDict, Dict, Iterator, List, Optional, Set
from unittest import result

import numpy as np

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult


from ..util.tag_check import is_popular_noun, is_tail, is_header, is_numeral, is_counter, is_form_tail, is_sahen, is_adverbable
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule
from spacy.tokens import Doc, Token

from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction, NounVectors

CONPOUND_DEP = 'compound'
KEEP_DEP = {'compound', 'nmod', 'obl', 'obj', 'nsubj', 'ROOT', 'acl'}
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

    def get_vector(self, complessed_noun_vectors) -> List[np.ndarray]:

        return [complessed_noun_vectors[token.norm_] for token in self.tokens]


type Nouns = DefaultDict[str, Set[Token]]


class Rule(KeywordExtractRule):
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:
        complex_word_tokens: Dict[str,
                                  ComplexWordDTO] = defaultdict(ComplexWordDTO)
        noun_vectors: NounVectors = {}
        nouns: Nouns = defaultdict(set)
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

                        complex_word_tokens, noun_vectors, nouns = self._update_section(canditate_tokens=canditate_tokens,
                                                                                        complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)

                        canditate_tokens = []
                    continue
                if token.pos_ == "NOUN":

                    if is_popular_noun.check(token=token) and len(list(token.children)) == 0:

                        if token.dep_ == CONPOUND_DEP:
                            is_canditate_exists = True
                            canditate_tokens.append(token)
                            continue

                        nouns[token.norm_].add(token)
                        noun_vectors[token.norm_] = token.vector
                        continue
                    if is_sahen.check(token=token):
                        nouns[token.norm_].add(token)
                        noun_vectors[token.norm_] = token.vector

            if is_canditate_exists == True:
                complex_word_tokens, noun_vectors, nouns = self._update_section(canditate_tokens=canditate_tokens,
                                                                                complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors)
        complessed_noun_vectors = projecter(noun_vectors)
        for complex_word, data in complex_word_tokens.items():

            sk = SpecifiedKeyword(
                headword=complex_word,
                vectors=data.get_vector(
                    complessed_noun_vectors=complessed_noun_vectors),
                is_force=data.is_force,
                source_ids=set(data.tokens)
            )
            results.add_keyword(sk)
        for norm, tokens in nouns:
            sk = SpecifiedKeyword(
                headword=complex_word,
                vectors=complessed_noun_vectors[norm],
                is_force=False,
                source_ids=tokens
            )
            results.add_keyword(sk)
        return results

    def _update_section(self, canditate_tokens: List[Token], complex_word_tokens: Dict[str, ComplexWordDTO], noun_vectors: NounVectors, nouns: Nouns):
        canditate_tokens_len = len(canditate_tokens)
        if canditate_tokens_len <= 1:
            return complex_word_tokens, noun_vectors
        tail_token = canditate_tokens[-1]
        if tail_token.dep_ == 'acl' or is_form_tail.check(token=token) == True:
            return complex_word_tokens, noun_vectors, nouns

        if canditate_tokens_len == 2:
            head_token = canditate_tokens[0]
            if is_sahen.check(token=tail_token) == True and is_sahen.check(head_token) == False:
                nouns[head_token.norm_].add(token)
                noun_vectors[head_token.norm_] = head_token.vector
                nouns[tail_token.norm_].add(tail_token)
                noun_vectors[tail_token.norm_] = tail_token.vector
                return complex_word_tokens, noun_vectors, nouns

        valid_results: List[Token] = []
        under_inspections = []
        is_valid_result_exist = False
        is_after_header = False
        is_after_header_exist = False
        is_numeral_only = False
        is_sahen_only = False
        is_under_inspection = False
        is_adverbable_exist = False
        for token in canditate_tokens:

            if is_after_header == False:
                if is_header.check(token=token):
                    is_after_header = True
                    under_inspections.append(token)
                    is_under_inspection = True
                    is_numeral_only = True
                    is_sahen_only = True
                    is_after_header_exist = False
                    continue
            else:
                if is_header.check(token=token):
                    if not (is_sahen_only or (is_numeral_only and is_counter.check(under_inspections[-1]))):
                        valid_results.extend(under_inspections)
                    under_inspections = []
                    under_inspections.append(token)
                    is_numeral_only = True
                    is_sahen_only = True
                    is_after_header_exist = False
                    is_adverbable_exist = False
                    continue
                is_after_header_exist = True
                if is_sahen.check(token=token):
                    is_adverbable_exist = False
                    is_sahen_only &= True
                    under_inspections.append(token)
                    continue
                else:
                    is_sahen_only = False
            if is_adverbable.check(token=token):
                is_under_inspection = True
                is_adverbable_exist = True
                under_inspections.append(token)
                is_sahen_only = False
                is_numeral_only = False

            if is_tail.check(token) and is_adverbable_exist:
                under_inspections = []
                is_under_inspection = False
                is_numeral_only = False
                is_sahen_only = False
                is_after_header_exist = False
                is_after_header = False
                is_adverbable_exist = False
                continue

            if is_numeral.check(token=token):
                if is_under_inspection == False:
                    is_under_inspection = True
                    is_numeral_only = True
                else:
                    is_numeral_only &= True
                is_sahen_only = False
                is_adverbable_exist = False
                under_inspections.append(token)
                continue
            if is_under_inspection == True:
                is_after_header = False
                is_under_inspection = False
                valid_results.extend(under_inspections)
                under_inspections = []
            is_valid_result_exist = True
            valid_results.append(token)
        if is_under_inspection:

            if is_after_header:

                if (is_after_header_exist == False) or (is_numeral_only == False and is_sahen_only == False):
                    is_valid_result_exist = True
                    valid_results.extend(under_inspections)
            else:
                if is_numeral_only == False:
                    is_valid_result_exist = True
                    valid_results.extend(under_inspections)
                else:
                    if not is_counter.check(under_inspections[-1]):
                        is_valid_result_exist = True
                        valid_results.extend(under_inspections)

        if not is_valid_result_exist:
            return complex_word_tokens, noun_vectors, nouns

        key = ''
        for token in valid_results:
            key += token.norm_
            noun_vectors[token.norm_] = token.vector
        data = complex_word_tokens[key]

        data.tokens += valid_results

        return complex_word_tokens, noun_vectors, nouns
