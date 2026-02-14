
from collections import defaultdict, deque
from typing import DefaultDict, Dict, Iterator, List, Optional, Set
import numpy as np
from data_loader.dto import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from ..util.tag_check import is_popular_noun, is_tail, is_header, is_numeral, is_counter, is_form_tail, is_sahen, is_adverbable
from doc2vec.spacy.components.keyword_extractor.protocol import ExtractResultDTO, KeywordExtractRule
from spacy.tokens import Doc, Token
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction, NounVectors
from ..stopwords import complex_token
from ginza import DetailedToken
import regex as re


CONPOUND_DEP = 'compound'
KEEP_DEP = {'compound', 'nmod', 'obl', 'obj', 'nsubj', 'ROOT', 'acl'}
MAIN_DEP = {'nsubj', 'ROOT'}
EMPTY_SET = set()

地名扱いの可能性がある漢数字に加えて漢字一文字のパターン = re.compile(r'^[零一二三四五六七八九十百千万憶兆]+\p{Han}$')


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
        exist_tokens = set()
        result = []
        for token in self.tokens:
            if token.norm_ in exist_tokens:
                continue
            exist_tokens.add(token.norm_)
            result.append(complessed_noun_vectors[token.norm_])
        return result


type Nouns = DefaultDict[str, Set[Token]]
形容的な接尾語 = {'用', '中', '前', '後', '上', '下', '性'}
年号 = {'明治', '大正', '昭和', '平成', '令和'}


class Rule(KeywordExtractRule):
    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO) -> List[SpecifiedKeyword]:
        complex_word_tokens: Dict[str,
                                  ComplexWordDTO] = defaultdict(ComplexWordDTO)
        noun_vectors: NounVectors = {}
        nouns: Nouns = defaultdict(set)
        is_overwrites = {}
        for sent in doc.sents:

            is_canditate_exists = False
            canditate_tokens: List[Token] = []
            for token in sent:

                if is_canditate_exists == True:

                    if token.dep_ in KEEP_DEP:
                        canditate_tokens.append(token)

                    else:

                        is_canditate_exists = False

                        complex_word_tokens, noun_vectors, nouns = self._update_section(canditate_tokens=canditate_tokens,
                                                                                        complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors, nouns=nouns)

                        canditate_tokens = []
                    continue

                if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                    if len(tuple(token.children)) != 0:
                        continue
                    if is_counter.check(token=token):
                        if token.i > 0 and is_numeral.check(doc[token.i - 1]):
                            continue

                    is_alone = True
                    for ancester in token.ancestors:
                        if ancester.pos_ == "NOUN":
                            is_alone = False
                            break
                    if is_alone:
                        continue
                    if token.dep_ == CONPOUND_DEP:
                        is_canditate_exists = True
                        canditate_tokens.append(token)
                        continue

                    if token.dep_ == "PROPN" or is_sahen.check(token=token):
                        nouns[token.norm_].add(token)

                        continue
                    if is_popular_noun.check(token=token):
                        is_sahen_exist = False
                        split_results: List[List[DetailedToken]
                                            ] = doc.user_data["sub_tokens"][token.i]
                        for detailed_tokens in split_results:
                            if len(detailed_tokens) != 2:
                                continue
                            tail_token = detailed_tokens[-1]
                            head_token = detailed_tokens[0]
                            if ('サ変' in tail_token.tag) and ('普通名詞' in head_token.tag):
                                is_sahen_exist = True
                                nouns[tail_token.norm].add(token)
                                is_overwrites[tail_token.norm] = False
                                head_key = ''
                                for head_token in detailed_tokens[:-1]:
                                    head_key += head_token.norm
                                nouns[head_key].add(token)
                                is_overwrites[head_key] = False
                                break
                        if is_sahen_exist == True:
                            continue
                        nouns[token.norm_].add(token)

            if is_canditate_exists == True:
                complex_word_tokens, noun_vectors, nouns = self._update_section(canditate_tokens=canditate_tokens,
                                                                                complex_word_tokens=complex_word_tokens, noun_vectors=noun_vectors, nouns=nouns)

        for complex_word, data in complex_word_tokens.items():
            if '法第' in complex_word:
                continue
            sk = SpecifiedKeyword(
                headword=complex_word,
                vectors=[],
                is_force=data.is_force,
                tokens=set(data.tokens)
            )
            results.add_keyword(sk)
        for norm, tokens in nouns.items():

            sk = SpecifiedKeyword(
                headword=norm,
                vectors=[],
                is_force=False,
                tokens=tokens
            )
            results.add_keyword(
                sk, is_overwrite_token=is_overwrites.get(norm, True))
        return results

    def _update_section(self, canditate_tokens: List[Token], complex_word_tokens: Dict[str, ComplexWordDTO], noun_vectors: NounVectors, nouns: Nouns):
        # print(canditate_tokens)
        canditate_tokens_len = len(canditate_tokens)
        if canditate_tokens_len <= 1:
            return complex_word_tokens, noun_vectors, nouns
        tail_token = canditate_tokens[-1]
        if tail_token.dep_ == 'acl' or is_form_tail.check(token=tail_token):

            return complex_word_tokens, noun_vectors, nouns

        if canditate_tokens_len == 2:
            if is_sahen.check(token=tail_token) == True:
                head_token = canditate_tokens[0]
                if is_header.check(head_token):
                    return complex_word_tokens, noun_vectors, nouns
                nouns[head_token.norm_].add(head_token)
                noun_vectors[head_token.norm_] = head_token.vector
                nouns[tail_token.norm_].add(tail_token)
                noun_vectors[tail_token.norm_] = tail_token.vector
                return complex_word_tokens, noun_vectors, nouns
            if tail_token.norm_ in 形容的な接尾語:
                return complex_word_tokens, noun_vectors, nouns

        valid_results: List[Token] = []
        valid_results_list: List[List[Token]] = [valid_results]
        under_inspections = []

        約の後の続きである = False
        約に続いてトークンが存在している = False
        is_numeral_only = True

        is_under_inspection = False

        limit = len(canditate_tokens)
        index = 0
        while index < limit:
            token = canditate_tokens[index]
            index += 1

            is_blockword, slide = complex_token.check(token=token)
            if is_blockword:
                index += slide
                continue

            if token.norm_ == '約':
                if 約の後の続きである:
                    if not is_numeral_only:

                        valid_results.extend(under_inspections)
                    else:
                        valid_results = []
                        valid_results_list.append(valid_results)
                else:
                    約の後の続きである = True

                約に続いてトークンが存在している = False
                under_inspections = []
                under_inspections.append(token)
                is_numeral_only = True

                continue
            約に続いてトークンが存在している = True

            if is_numeral.check(token=token) or token.norm_ in 年号 or 地名扱いの可能性がある漢数字に加えて漢字一文字のパターン.search(token.norm_) is not None:
                if is_under_inspection == False:
                    is_under_inspection = True
                    is_numeral_only = True
                else:
                    is_numeral_only &= True

                under_inspections.append(token)
                continue

            if is_under_inspection == True:
                if is_numeral_only and not is_tail.check(token):

                    valid_results = []
                    valid_results_list.append(valid_results)
                else:
                    valid_results.extend(under_inspections)

                約の後の続きである = False
                is_under_inspection = False
                is_numeral_only = False
                under_inspections = []

            valid_results.append(token)
        if is_under_inspection:

            if 約の後の続きである:

                if (約に続いてトークンが存在している == False) or (is_numeral_only == False):

                    valid_results.extend(under_inspections)
            else:
                if is_numeral_only == False or not is_counter.check(under_inspections[-1]):
                    valid_results.extend(under_inspections)

        for valid_results in valid_results_list:
            key = ''
            for token in valid_results:
                key += token.lemma_
                noun_vectors[token.norm_] = token.vector
            if not key:
                continue
            # print(key)
            data = complex_word_tokens[key]
            data.tokens += valid_results

        return complex_word_tokens, noun_vectors, nouns
