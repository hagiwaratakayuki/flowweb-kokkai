from collections import defaultdict

from typing import Callable, Dict, List, Set

import numpy as np
from regex import T

from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from processer.doc2vec.tokenaizer.japanese_language.extracter.basic import sahen

from ..stopwords import remove_stopwords
from ..util.tag_check import is_sahen, is_adverbable, is_tail, is_numeral, is_popular_noun
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc, Token

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
        sahen_dict = {}
        popular_noun_dict = {}

        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:

                if token.pos_ == "NOUN":
                    count = 0
                    is_popular_noun_flag, is_sahen_flag = self._check_noun_type(
                        token=token, popular_noun_dict=popular_noun_dict, sahen_dict=sahen_dict)
                    if token.pos_ == "NOUN" and is_popular_noun_flag == True or is_sahen_flag == True:
                        path_tokens = []

                        is_token_add = False

                        is_include_popular = is_popular_noun_flag
                        for ancester in token.ancestors:
                            if ancester.pos_ == "NOUN":
                                is_ancester_populer_noun_flag, is_ancester_sahen_flag = self._check_noun_type(
                                    token=ancester, popular_noun_dict=popular_noun_dict, sahen_dict=sahen_dict)
                                if is_ancester_populer_noun_flag == True:
                                    is_include_popular = True
                                is_sahen_flag = is_sahen.check(token=ancester)
                                if is_ancester_populer_noun_flag or is_ancester_sahen_flag == True:
                                    if is_token_add == False and ancester.i > token.i:
                                        is_token_add = True
                                        path_tokens.append(token.i)
                                        count += 1
                                count += 1
                                path_tokens.append(ancester.i)
                        if is_token_add == False:
                            path_tokens.append(token.i)
                            count += 1
                        if count <= 1 or not is_include_popular:
                            continue
                        """
                        noun_data = noun_datas[token.norm_]
                        noun_data.faces.add(token.orth_)
                        noun_data.faces.add(token.lemma_)
                        noun_data.faces.add(token.norm_)
                        faces |= noun_data.faces
                        noun_data.source_ids.add(token.i)
                        noun_data.is_force = False
                        noun_vectors[token.norm_] = token.vector
                        noun_datas[token.norm_] = noun_data"
                        """
        projected_noun_vectors = projecter(noun_vectors)
        removed_words = set(remove_stopwords(list(faces)))

        for noun, data in noun_datas.items():
            if (data.faces & removed_words) != data.faces:
                continue
            sk = SpecifiedKeyword(
                headword=noun, vector=projected_noun_vectors[noun], is_force=data.is_force, source_ids=data.source_ids)
            results.add_keyword(sk)
        return results

    def _check_noun_type(self, token: Token, popular_noun_dict, sahen_dict):
        if token.i in popular_noun_dict:
            is_popular_noun_flag = popular_noun_dict[token.i]
        else:
            is_popular_noun_flag = is_popular_noun.check(token=token)
            popular_noun_dict[token.i] = is_popular_noun_flag
        if token.i in sahen_dict:
            is_sahen_flag = sahen_dict[token.i]
        else:
            is_sahen_flag = is_sahen.check(token=token)
            sahen_dict[token.i] = is_sahen_flag
