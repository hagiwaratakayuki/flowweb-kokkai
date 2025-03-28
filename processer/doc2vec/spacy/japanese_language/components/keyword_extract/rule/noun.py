from collections import defaultdict, deque


from typing import Any, Callable, DefaultDict, Deque, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple


import numpy as np


from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.spacy.japanese_language.components.keyword_extract.util.keyword_match.is_nengou import 年号であるか否か


from ..stopwords import remove_stopwords
from ..util.tag_check import is_popular_noun
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule
from spacy.tokens import Doc, Token

from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction


EMPTY_SET = set()


class Rule(KeywordExtractRule):
    def __init__(self, noun_stopword_remover=remove_stopwords):
        self._noun_stopword_remover = noun_stopword_remover

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:

        noun_2_vec = {}
        headword_2_token_ids = defaultdict(set)

        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:
                is_propn = token.pos_ == "PROPN" and 年号であるか否か(
                    token=token, is_negative_match=True)
                if token.pos_ != "NOUN" and is_propn == False:
                    continue

                if is_popular_noun.check(token=token) == False:
                    continue

                if is_propn == True:
                    is_keyword = True
                else:
                    is_keyword = True
                    has_ancester_noun = False
                    for ancester in token.ancestors:
                        if ancester.pos_ == "NOUN" and is_popular_noun.check(token=token) == True:
                            has_ancester_noun = True
                            is_keyword &= ancester.vector_norm < token.vector_norm
                    is_keyword &= has_ancester_noun
                if is_keyword == True:
                    noun_2_vec[token.norm_] = token.vector
                    headword_2_token_ids[token.norm_].add(token)
        noun_2_vec = projecter(noun_2_vec)

        for headword, source_ids in headword_2_token_ids.items():
            keyword = SpecifiedKeyword(
                headword=headword, source_ids=source_ids, vectors=[noun_2_vec[headword]])
            results.add_keyword(keyword=keyword)
        return results
