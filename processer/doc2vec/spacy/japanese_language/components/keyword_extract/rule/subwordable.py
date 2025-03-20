from collections import defaultdict, deque

import token
from typing import Any, Callable, DefaultDict, Deque, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

from ginza import set_split_mode, sub_tokens, tag
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


class SubwordedWordDTO:

    tokens: Dict[Token, Iterable[Token]]
    sub_detail: Optional[str]

    def __init__(self):
        self.tokens = {}
        self.sub_detail = None

    def append(self, head_token: Token, sub_tokens: Iterable[Token], sub_detail):
        self.tokens[head_token] = sub_tokens
        self.sub_detail = sub_detail


EMPTY_SET = set()


class Rule(KeywordExtractRule):
    def __init__(self, noun_stopword_remover=remove_stopwords, subword_remover=None):
        self._noun_stopword_remover = noun_stopword_remover
        self._subword_remover = subword_remover

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, projecter: ProjectFunction) -> List[SpecifiedKeyword]:
        # sub detail周りの処理を追加
        wordtuple_2_token_dict = defaultdict(SubwordedWordDTO)
        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:

                if token.pos_ != "PROPN" and token.pos_ != "NOUN" and is_popular_noun.check(token=token) == False:
                    continue
                has_subword = False
                subwords: Deque[Token] = deque()
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
                    if is_sahen.check(token=ancester):
                        subwords.append(ancester)
                        has_subword = True
                if not has_subword:
                    continue
                if not headword:
                    headword = token.norm_
                sub_nouns = (sub_detail, )
                for subword in subwords:
                    sub_nouns += (subword.norm_,)
                wordtuple_2_token_dict[(
                    headword, sub_detail, sub_nouns,)].append(head_token=token, sub_tokens=subwords, sub_detail=sub_detail)
        sub_tokens: Set[Token] = set()
        for wordtuple, swdto in wordtuple_2_token_dict.items():

            head_sub_paires = set()
            head_tokens = set(swdto.token_dict.keys())
            head_keywords = results.get_by_source_ids(head_tokens)
            for keyword in head_keywords.values():
                target_head_tokens = head_tokens & keyword.source_ids

                for target_head_token in target_head_tokens:
                    subkey = frozenset()
                    sub_tokens = set(swdto.tokens[target_head_token])
                    included_tokens = keyword.source_ids & sub_tokens
                    for sub_token in included_tokens:
                        subkey &= frozenset([sub_token.norm_])

                    key = (keyword.id, subkey,)
                    if key in head_sub_paires:
                        continue
                    head_sub_paires.add(key)

                    if swdto.sub_detail != None:
                        if swdto.sub_detail in keyword.headword:
                            keyword.headword = wordtuple[0]
                            if swdto.sub_detail not in keyword.subwords:
                                keyword.add_subword(swdto.sub_detail)
                    if included_tokens == sub_tokens:
                        continue
                    add_tokens = set()
                    for sub_token in swdto.tokens[target_head_token]:
                        if sub_token in included_tokens:
                            continue
                        add_tokens.add(sub_token)
                        keyword.add_subword(sub_token.norm_)
                    results.add_tokens(keyword=keyword, tokens=add_tokens)
            # 既存キーワード中にサ変が含まれるケース
            for head_token, sub_tokens in swdto.tokens.items():
                for keyword in results.get_by_source_ids(sub_tokens).values():
                    if head_token in keyword.source_ids:
                        continue
                    for paires in keyword.to_paires():
                        pass
