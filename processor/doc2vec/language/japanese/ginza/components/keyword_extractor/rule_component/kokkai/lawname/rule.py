

from calendar import c
from typing import Any, DefaultDict, Deque, Iterator, List, Literal, Optional, Set, Tuple, Union


from more_itertools import first
import numpy as np


from doc2vec.util.specified_keyword import SpecifiedKeyword, EqIn
import regex as re

from spacy.tokens import Doc

import json
import os
from collections import defaultdict
from operator import itemgetter
from collections import Counter, defaultdict, deque
from data_loader.kokkai import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.keyword_extractor.protocol import ExtractResultDTO, KeywordExtractRule
from doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.discussion_context import DiscussionContext
from doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.chapter import extract_chapter_expressions, 章としての区分を表す単語
from doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.dtos import LawDTO, LawDTOList
from doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.types import IsCountChapterFlag, カタカナ章表現を示すフラグ
from doc2vec.spacy.components.nlp.loader import load_matcher


zerogetter = itemgetter(0)
グループ分け単語 = set('編章節款目')
章とグループ分けの単語 = set(章としての区分を表す単語) | グループ分け単語
区分の最大深さ = len(章としての区分を表す単語) - 1
カナ区分の深さ = 区分の最大深さ + 1

章区分を表すパターンと分割パターンのペアのリスト = [
    (re.compile(r'(第?\d[' + 章としての区分を表す単語 + r'の、]*)+\p{Katakana}*'),
     re.compile(r'(\d+|の、?\p{Katakana}+)([' + 章としての区分を表す単語 + r'、]?)'),)

]


アイヌ新法 = "アイヌ新法"
改正前のアイヌ新法の正式名称 = "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律"


活火山法 = "活火山法"
活火山法の略称候補 = re.compile("活動?火山法")

改正前の活火山法の正式名称 = "活動火山周辺地域における避難施設等の整備等に関する法律"
改正後の活火山法の正式名称 = "活動火山対策特別措置法"
name_index_path = os.path.realpath(
    'process_data/law/nameindex.json')
ryakusyou_tenchi_path = os.path.realpath(
    'process_data/law/ryakusyou_tenchi.json')
ryakusyou_path = os.path.realpath(
    'process_data/law/ryakusyou.json')
with open(file=name_index_path, mode='r', encoding="utf-8") as fp:
    name_index = json.load(fp)
with open(file=ryakusyou_path, mode='r', encoding="utf-8") as fp:
    略称と正式名称の対応表 = json.load(fp)

with open(file=ryakusyou_tenchi_path, mode='r', encoding="utf-8") as fp:
    ryakusyou_tench = json.load(fp)
law_standard_phrases = ['法の下の平等', '法の支配']
商売の方法または金商法の略称の一部としての商法を表すパターン = re.compile(r'\p{Han}+商法')
漢字でないパターン = re.compile(r'^[^\p{Han}]')

連続章段階表現の接続語 = {'の', '第'}
記号を表すパターン = re.compile(r'^\W+$')
数字と第を表すパターン = re.compile(r'\d|第')

並列を表す日本語のパターン = [
    re.compile('と$'),
    re.compile('並びに?$|ならびに?$'),
    re.compile('び$')
]
DUMMY_SET = {0}


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


class Cursor:
    def __init__(self, doc: Doc):
        self.doc_len = len(doc)
        self.index = -1
        self.limit = self.doc_len - 1
        self.doc = doc
        self.token_len = 0
        self._check_next()
        self.position = 0

    def _check_next(self):
        self.has_next = self.index < self.limit

    def get_next(self):
        if self.has_next == True:
            return self.doc[self.index + 1]
        return False

    def step(self):

        if self.has_next:
            self.index += 1
            self.position += self.token_len
            self.now = self.doc[self.index]
            self.token_len = len(self.now)
            self._check_next()
            return True

        return False


class ChaptersAndTokens:
    def __init__(self) -> None:
        self.tokens = deque()
        self.chapters = deque()


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, model_name: str):

        reverse_dict = defaultdict(set)

        all_text = doc.text
        law_count = all_text.count('法')
        if law_count == 0 and self.context.get_data(dto=dto)[0] == False:

            return results
        standard_phrase_count = 0
        detected_phrases = set()
        additional_law_words = set()
        for phrase in law_standard_phrases:
            detected_phrase_count = all_text.count(phrase)

            standard_phrase_count += detected_phrase_count
            if detected_phrase_count > 0:
                detected_phrases.add(phrase)
        for detected_phrase in detected_phrases:

            results.add_keyword(SpecifiedKeyword(
                headword=detected_phrase, is_force=True, tokens={1}))

        if law_count == standard_phrase_count:
            return results
        商売の方法または金商法の略称の一部としての商法である = False

        target_tokens = deque()

        canditates_set = set()
        ryakusyou_canditates_set = set()
        law_list = LawDTOList()
        アイヌ新法が含まれるか = アイヌ新法 in doc.text

        if アイヌ新法が含まれるか is True:
            if dto.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称

            self._set_law_positions(
                doc, law_list=law_list, lawname=アイヌ新法の正式名称, face=アイヌ新法)
            self._get_hittokens(doc=doc, word=アイヌ新法, tokens=target_tokens)

        活火山法の検索結果 = 活火山法の略称候補.search(doc.text)
        活火山法が含まれるか = 活火山法の検索結果 is not None
        if 活火山法が含まれるか is True:
            additional_law_words.add(活火山法)
            活火山法の略称 = 活火山法の検索結果.group(0)
            if dto.published >= "1973-7-13":
                活火山法の正式名称 = 改正後の活火山法の正式名称
            else:
                活火山法の正式名称 = 改正前の活火山法の正式名称
            self._set_law_positions(
                doc, law_list=law_list, lawname=活火山法の正式名称, face=活火山法の略称)

            self._get_hittokens(doc=doc, word=活火山法の略称, tokens=target_tokens)
        改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in doc.text
        改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in doc.text
        if 改正前の活火山法の正式名称が存在する or 改正後の活火山法の正式名称が存在する:
            additional_law_words.add(活火山法)
            if 改正前の活火山法の正式名称が存在する:

                self._get_hittokens(doc, word=改正前の活火山法の正式名称,
                                    tokens=target_tokens)
            if 改正後の活火山法の正式名称が存在する:

                self._get_hittokens(
                    doc=doc, word=改正後の活火山法の正式名称, tokens=target_tokens)

        for i in range(len(doc.text) - 1):
            gram = doc.text[i:i + 2]
            canditates_set.update(name_index.get(gram, []))

            ryakusyou_canditates_set.update(
                ryakusyou_tench.get(gram, []))

        略称の可能性があるもののリスト = [
            canditate for canditate in ryakusyou_canditates_set if canditate in doc.text]

        ryakusyou_index = [EqInShorter(ry) for ry in 略称の可能性があるもののリスト]
        発見された正式名称のリスト = [
            canditate for canditate in canditates_set if canditate in doc.text and canditate not in ryakusyou_index]

        正式名称のインデックス = [EqInShorter(正式名称)
                       for 正式名称 in 発見された正式名称のリスト]

        法律名の略称のリスト = [
            canditate for canditate in 略称の可能性があるもののリスト if canditate not in 正式名称のインデックス]
        for 法律名の略称 in 法律名の略称のリスト:
            if 法律名の略称 == アイヌ新法 or 法律名の略称 == 活火山法:
                continue

            reverse_dict[略称と正式名称の対応表[法律名の略称]].add(法律名の略称)
        if "商法" in 発見された正式名称のリスト:

            商売の方法または金商法の略称の一部としての商法である |= 商売の方法または金商法の略称の一部としての商法を表すパターン.search(
                doc.text) is not None

        for 法律名 in 発見された正式名称のリスト:
            self._set_law_positions(doc, law_list=law_list, lawname=法律名)

        for 法律名の略称 in 法律名の略称のリスト:
            法律の正式名称 = 略称と正式名称の対応表[法律名の略称]
            self._set_law_positions(
                doc=doc, law_list=law_list, lawname=法律の正式名称, face=法律名の略称)

        # line_laws.extend((m.group(0), m.start(), section_rank[m.group(1)], )
        #             )

        is_context_added = False

        if law_list.len == 0:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if not is_context_exist:
                return results
            law_dto = LawDTO(name=法律名, start=0, end=0, is_guess=True)
            law_list.append(law_dto)

        else:
            law_list.sort()
            first = law_list.get_first()
            if first.start != 0:
                law_dto = LawDTO(name=first.name, start=0,
                                 end=0, is_guess=True)
                law_list.prepend(law_dto)

        extract_chapter_expressions(
            doc=doc, law_dto_list=law_list, model_name=model_name)
        while law_list.step():
            law_dto = law_list.now
            # 結果への反映処理

        return results
