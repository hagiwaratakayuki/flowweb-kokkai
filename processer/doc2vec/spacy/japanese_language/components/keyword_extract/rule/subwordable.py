from collections import defaultdict, deque


from typing import Any, Callable, DefaultDict, Deque, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple, Union


from ginza import norm
import numpy as np


from data_loader.dto import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.protocol import SpacySpecifiedKeyword as SpecifiedKeyword


from ..stopwords import remove_stopwords
from ..util.tag_check import is_sahen, is_adverbable, is_tail, is_numeral, is_popular_noun
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc, Token

from doc2vec.spacy.components.commons.projections_protocol import ProjectFunction
from doc2vec.spacy.components.commons.const import SPECIFIABLE_POS


class SubwordedWordDTO:

    tokens: Dict[Token, List[Token]]
    sub_detail: Optional[str]

    def __init__(self):
        self.tokens = {}
        self.sub_detail = None

    def append(self, head_token: Token, sub_tokens: List[Token], sub_detail):
        self.tokens[head_token] = sub_tokens
        self.sub_detail = sub_detail


EMPTY_SET = set()


class Rule(KeywordExtractRule):
    def __init__(self, noun_stopword_remover=remove_stopwords, subword_remover=None):
        self._noun_stopword_remover = noun_stopword_remover
        self._subword_remover = subword_remover

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:
        doc_i_max = len(doc) - 1
        paire_to_keyword: Dict[FrozenSet, SpecifiedKeyword] = {}
        canditate_tokens: Set[Token] = set()
        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:
                norm_to_vectors = {}
                if token.dep_ == 'compound' or (token.pos_ != "PROPN" and not (token.pos_ == "NOUN" and is_popular_noun.check(token=token) == True)):
                    continue
                _token = token
                for child in token.children:
                    if child.dep_ == 'compound' or (child.pos_ != "PROPN" and not (child.pos_ == "NOUN" and is_popular_noun.check(token=child) == True)):
                        continue
                    if _token.i < child.i:
                        continue
                    ancesters_set = set(child.ancestors)
                    if token not in ancesters_set:
                        continue
                    _token = child

                canditate_tokens.add(_token)
        for token in canditate_tokens:
            has_subword = False
            sub_words: List[Token] = []
            sub_detail = None

            headword = ''
            for detailed_tokens in doc.user_data["sub_tokens"][token.i]:
                if len(detailed_tokens) == 0:
                    continue
                tail_token = detailed_tokens[-1]
                if 'サ変' in tail_token.tag:
                    has_subword = True
                    sub_detail = tail_token.norm
                    for detailed_token in detailed_tokens[:-1]:
                        headword += detailed_token.norm

            for ancester in token.ancestors:
                if is_sahen.check(token=ancester) == False:
                    continue
                if ancester.i < doc_i_max and is_tail(doc[ancester.i + 1]) == True:
                    continue
                sub_words.append(ancester)
                has_subword = True
            if not has_subword:
                continue

            subwords_set = set(sub_words)

            token_keyword_paths: Deque[Tuple[Optional[SpecifiedKeyword],
                                             Tuple[Union[Token, SpecifiedKeyword]], Set[Any]]] = deque()

            if token in results.token_id_2_keyword:
                has_subword = False
                for keyword in results.get_by_source_ids([token]):
                    if keyword.source_ids >= subwords_set:
                        if sub_detail != None:
                            keyword.set_headword(headword=headword)
                            keyword.add_subword(sub_detail)
                        continue
                    has_subword = True
                    token_keyword_paths.append(
                        (keyword, (), subwords_set - keyword.source_ids,))
            else:
                token_keyword_paths.append(
                    (None, (), subwords_set - keyword.source_ids,))
            if not has_subword:
                continue
            for sub_word in sub_words:
                norm_to_vectors[sub_word.norm_] = sub_word.vector
                next_token_keyword_paths = deque()
                sub_keywords = results.token_id_2_keyword.get(
                    sub_word, None)
                for head_keyword, path_steps, least_tokens_set in token_keyword_paths:

                    if sub_word not in least_tokens_set:
                        next_token_keyword_paths.append(
                            (head_keyword, path_steps, least_tokens_set))
                    else:
                        if sub_keywords == None:
                            next_token_keyword_paths.append(
                                head_keyword, path_steps + (token,), least_tokens_set)
                        else:
                            for sub_keyword in sub_keywords.values():
                                next_token_keyword_paths.append(
                                    head_keyword, path_steps + (sub_keyword,), least_tokens_set - sub_keyword.source_ids)
                token_keyword_paths = next_token_keyword_paths
            norm_to_vectors = projecter(norm_to_vectors)
            min_i = token.i

            target_i = token.i - 1
            while target_i >= 0:
                target_token = doc[target_i]
                if target_token.dep_ != 'compound':
                    break
                min_i = target_i
                target_i -= 1
            tail_word = sub_words[-1]
            max_i = tail_word.i

            if tail_word.dep_ == 'compound':
                target_i = max_i + 1
                while target_i <= doc_i_max:
                    target_token = doc[target_i]
                    if target_token.POS_ != 'NOUN':
                        break
                    max_i = target_i
                    target_i += 1

            for head_keyword, path_steps, least_tokens_set in token_keyword_paths:
                head_keywords: Deque[Tuple[SpecifiedKeyword, List]] = deque(
                )
                if head_keyword == None:
                    if sub_detail != None:
                        subwords = [sub_detail]
                    else:
                        subwords = []
                    head_keyword = SpecifiedKeyword(
                        headword=headword, vectors=[], subwords=subwords, source_ids={token})
                    head_keywords.append((head_keyword, [],))
                else:
                    source_ids = {
                        source_token for source_token in head_keyword.source_ids if min_i <= source_token.i <= max_i}
                    if head_keyword.source_ids > source_ids:
                        head_keyword_ = head_keyword.clone()
                        head_keyword.source_ids -= source_ids
                        head_keyword_.source_ids = source_ids
                        head_keywords.append((head_keyword_, [],))
                    else:
                        head_keywords.append((head_keyword, [],))

                for path_step in path_steps:
                    if isinstance(path_step, Token):
                        for head_keyword, vectors in head_keywords:
                            head_keyword.add_subword(path_step.norm_)
                            head_keyword.source_ids.add(path_step)
                            vectors.append(
                                norm_to_vectors[path_step.norm_])
                    else:
                        source_ids = {
                            step for step in path_step.source_ids if min_i <= step.i <= max_i}
                        path_step.source_ids -= source_ids
                        next_head_keywords = deque()

                        for head_keyword, vectors in head_keywords:
                            paires = keyword.to_paires()
                            len_paire = len(paires)
                            for paire in paires:

                                if len_paire <= 1:
                                    _head_keyword = head_keyword
                                    _vectors = vectors

                                else:

                                    _head_keyword = head_keyword.clone()
                                    _vectors = vectors[:]
                                len_paire -= 1
                                _head_keyword.add_subword(paire)
                                _head_keyword.source_ids += source_ids
                                _vectors.extend(path_step.vectors)
                                next_head_keywords.append(
                                    (_head_keyword, _vectors,))

                        head_keywords = next_head_keywords
                for head_keyword, vectors in head_keywords:
                    head_keyword.vectors.extend(vectors)

                    paire_set = frozenset(keyword.to_paires())
                    if paire_set in paire_to_keyword:
                        paire_to_keyword[paire_set].source_ids += head_keyword.source_ids
                        continue

                    paire_to_keyword[paire_set] = keyword

                    results.add_keyword(head_keyword, False)
        return results
