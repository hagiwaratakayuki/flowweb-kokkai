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
        # sub detail周りの処理を追加
        wordtuple_2_token_dict = defaultdict(SubwordedWordDTO)
        for noun_chunk in doc.noun_chunks:

            for token in noun_chunk:

                if token.pos_ != "PROPN" and token.pos_ != "NOUN" and is_popular_noun.check(token=token) == False:
                    continue
                has_subword = False
                subwords: List[Token] = []
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
        # 型推論が効かないので型定義
        sub_tokens_set: Set[Token] = set()
        for wordtuple, swdto in wordtuple_2_token_dict.items():

            head_tokens = set(swdto.token_dict.keys())
            keyword_id_to_head_tokens = defaultdict(deque)
            is_linked_head_exist = False
            is_not_linked_head_exist = False
            not_linked_heads = deque()
            for head_token in head_tokens:
                linked_keywords = results.token_id_2_keyword.get(
                    head_token, None)
                if linked_keywords == None:
                    not_linked_heads.append(head_token)
                    is_not_linked_head_exist = True
                    continue
                is_linked_head_exist = True
                for linked_keyword_id in linked_keywords.keys():
                    keyword_id_to_head_tokens[linked_keyword_id].append(
                        head_token)

            if is_linked_head_exist == True:
                for keyword_id, head_tokens in keyword_id_to_head_tokens.items():
                    keyword = results.keywords[keyword_id]
                    is_extend_tokens_exist = False
                    extend_tokens = {}

                    for head_token in head_tokens:
                        sub_tokens_set = set(swdto.tokens[head_token])
                        least_sub_token = sub_tokens_set - keyword.source_ids
                        if least_sub_token == EMPTY_SET:
                            continue
                        is_extend_tokens_exist = True
                        extend_tokens[head_token] = least_sub_token
                    if is_extend_tokens_exist == False:
                        continue
                    # パスを作って回す、に変更
                    # ここから下を共通化
                    all_link_paths = []

                    for head_token, least_sub_token in extend_tokens.items():
                        link_paths = [(least_sub_token, ())]
                        for sub_token in swdto.tokens[head_token]:
                            next_link_path = []
                            for path_least_sub_token, nodes in link_paths:
                                if sub_token not in path_least_sub_token:
                                    next_link_path.append(
                                        (path_least_sub_token, nodes,))
                                    continue
                                # パスごとの追加作業　tokenはnorm_に変換
                                is_linked_sub_keywords_exist = False
                                is_first = True
                                for linked_sub_keywords in results.token_id_2_keyword.get(sub_token, []):
                                    is_linked_sub_keywords_exist = True

                                least_sub_token -= sub_token
                            link_paths = next_link_path
                        # nodeのみ追加するように
                        all_link_paths.extend(link_paths)

            head_keywords = results.get_by_source_ids(head_tokens)
            remove_keywords = deque()
            for keyword in head_keywords.values():
                target_head_tokens = head_tokens & keyword.source_ids

                for target_head_token in target_head_tokens:
                    all_tokens = {target_head_token} | set(
                        swdto.tokens[target_head_token])

                    if keyword.source_ids >= all_tokens:
                        continue
                    target
                    for sub_token in swdto.tokens[target_head_token]:

                        # 既存キーワード中にサ変が含まれるケース
            for head_token, sub_tokens_set in swdto.tokens.items():
                for keyword in results.get_by_source_ids(sub_tokens_set).values():
                    if head_token in keyword.source_ids:
                        continue
                    for paires in keyword.to_paires():
                        pass
