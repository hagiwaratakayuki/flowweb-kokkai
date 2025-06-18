

from multiprocessing import context
from tkinter import NO
from turtle import position
from typing import Deque, Iterator, List, Optional, Set, Tuple, Option
from unittest import result


import numpy as np


from crowler.lib.webapi.twitter import K
from doc2vec.util.specified_keyword import SpecifiedKeyword, EqIn
import regex as re

from spacy.tokens import Token, Doc, Span
import os
import json
from operator import attrgetter, itemgetter
from collections import Counter, defaultdict, deque
from data_loader.kokkai import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule
from doc2vec.spacy.japanese_language.components.keyword_extract.rule.kokkai.discussion_context import DiscussionContext


startkey = attrgetter('start')
zerogetter = itemgetter(0)

章としての区分を表す単語 = r"編章条項節款目"
区分の最大深さ = len(章としての区分を表す単語) - 1


章区分を表すパターンと分割パターンのペアのリスト = [
    (re.compile(r'(\d[' + 章としての区分を表す単語 + r'第の、]*)+\p{Katakana}*'),
     re.compile(r'(\d+|の、?\p{Katakana}+)([' + 章としての区分を表す単語 + '、]?)'),)

]

章の区分と数値の変換表 = {章としての区分を表す単語[i]: i for i in range(len(章としての区分を表す単語))}


スーパー301条対策のパターン = re.compile('ス.パ.')
委員会 = "委員会"


アイヌ新法 = "アイヌ新法"
改正前のアイヌ新法の正式名称 = "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律"


活火山法 = "活火山法"
活火山法の略称候補 = re.compile("活動?火山法")

改正前の活火山法の正式名称 = "活動火山周辺地域における避難施設等の整備等に関する法律"
改正後の活火山法の正式名称 = "活動火山対策特別措置法"
name_index_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/nameindex.json')
ryakusyou_tenchi_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/ryakusyou_tenchi.json')
ryakusyou_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/ryakusyou.json')
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


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


class LawDTO:
    start: int
    is_reverse: bool
    face: str
    name: str

    def __init__(self, name, start, face=''):
        self.name = name
        self.start = start
        self.face = face
        self.is_reverse = False
        self.len = len(self.get_face())
        self.end = self.start + self.len - 1

    def get_face(self):
        return self.face or self.name


class PositionList:
    positions: List[Tuple[float, float]]
    index: int
    now_start: int
    now_end: int

    def __init__(self):
        self.positions = []
        self.index = -1

    def append_position(self, start, end):
        self.positions.append((start, end,))

    def sort(self):
        self.positions.sort(key=zerogetter)
        self.limit = len(self.positions) - 1

    def step(self):

        self.index += 1
        if self.limit < self.index:
            return False
        start, end = self.positions[self.index]
        self.now_start = start
        self.now_end = end
        return True


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
            self.position += len(self.token_len)
            self.now = self.doc[self.index]
            self.token_len = len(self.now)
            self._check_next()
            return True
        return False


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO):

        law_index = defaultdict(set)
        reverse_dict = defaultdict(set)
        sent_number = -1
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

            results.append(SpecifiedKeyword(
                headword=detected_phrase, is_force=True))

        if law_count == standard_phrase_count:
            return results
        商売の方法または金商法の略称の一部としての商法である = False

        target_tokens = deque()
        law_2_overwrite = {}

        sent_number += 1

        canditates_set = set()
        ryakusyou_canditates_set = set()
        law_list: List[LawDTO] = []
        アイヌ新法が含まれるか = アイヌ新法 in doc.text

        if アイヌ新法が含まれるか is True:
            if dto.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称

            self._set_law_positions(doc, アイヌ新法の正式名称, アイヌ新法)
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

        law_list.sort(key=startkey)
        target_law_index = 0
        law_list_len = len(law_list)
        doc_len = len(doc)
        is_context_added = False
        position_list = PositionList()
        if law_list_len == 0:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if not is_context_exist:
                return results
            law_dto = LawDTO(name=法律名, start=0)
            law_list.append(law_dto)
            position_list.append_position(law_dto.start, law_dto.end)
            is_context_added = True
            law_list_len = 1

        law_expressions = set()

        token_len = 0
        cursor = Cursor(doc)
        段階表現のリスト = []

        段階表現と位置のインデックス = {}

        index = 0
        倒置表現の可能性がある限界 = len(doc.text) - 2

        for パターン, 分割パターン in 章区分を表すパターンと分割パターンのペアのリスト:
            for match in パターン.finditer(doc.text):
                all_text = match.group(0)
                倒置表現である = False
                if all_text[-1] == 'の':
                    match_end = match.exnd()
                    if match.end() > 倒置表現の可能性がある限界 or all_text[match_end] != '、' or 数字と第を表すパターン.search(all_text[match_end + 1]) == None:
                        倒置表現である = False
                    else:
                        倒置表現である = True
                段階表現のリスト.append(
                    (match.start(), 分割パターン.findall(all_text), 倒置表現である, ))
                段階表現と位置のインデックス[match.start()] = index
                position_list.append(match.start(), match.end())

        法律名のインデックス = -1
        for law_dto in law_list:
            法律名のインデックス += 1
            next_position = law_dto.start + law_dto.len
            リンクしている段階表現のID = 段階表現と位置のインデックス.get(next_position)
            if リンクしている段階表現のID is not None:

                law_dto.is_reverse = 段階表現のリスト[リンクしている段階表現のID][2]

            elif doc.text[next_position] in 連続章段階表現の接続語:  # 『憲法の、第9条』と『9条ですね、憲法の』、みたいな倒置表現
                リンクしている段階表現のID = 段階表現と位置のインデックス.get(
                    next_position + 1) or 段階表現と位置のインデックス.get(next_position + 2) or 段階表現と位置のインデックス.get(next_position + 3)
                if リンクしている段階表現のID is not None:
                    law_dto.is_reverse = 段階表現のリスト[リンクしている段階表現のID][2]
                else:

                    law_dto.is_reverse = doc.text[next_position] == 'の'

        next_law_position = doc_len

        law_dto = law_list[0]
        if not is_context_added:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if is_context_exist and law_dto.name != 法律名 and law_dto.start != 0:
                law_dto = LawDTO(name=法律名, start=0)
                law_list.insert(0, law_dto)
                law_list_len += 1

        段階表現のリストの長さ = len(段階表現のリスト)
        段階表現リストの行番号 = 段階表現のリストの長さ - 1

        law_list_index = law_list_len - 1

        段階表現のスタート, 段階表現, 倒置表現フラグ = 段階表現のリスト[段階表現リストの行番号]
        prev_law_dto: LawDTO = None
        law_dto = None
        段階表現の基準深さ = -1
        以前の段階表現の基準深さ = -1
        末尾はカナ表現か = False
        倒置の直後である = False
        現在の章表現 = None
        未判定の段階表現のdeque = deque()
        法律名と段階表現の対応表 = defaultdict(set)
        法律名の一覧 = set()
        while law_list_index >= 0:

            prev_law_dto = law_dto
            以前の段階表現の基準深さ = 段階表現の基準深さ
            段階表現の基準深さ = -1
            law_dto = law_list[law_list_index]
            法律名の一覧.add(law_dto.name)
            law_list_index = 1

            is_tail = True

            while 段階表現のスタート > next_law_position:
                if is_tail == True:
                    is_tail = False
                    if prev_law_dto != None and prev_law_dto.is_reverse:
                        target_law = prev_law_dto
                        現在の段階表現の基準深さ = 以前の段階表現の基準深さ
                        倒置の直後である = True

                    else:
                        target_law = prev_law_dto
                        倒置の直後である = False
                        現在の段階表現の基準深さ = 段階表現の基準深さ
                        末尾はカナ表現か = False
                else:
                    target_law = law_dto
                    現在の段階表現の基準深さ = 段階表現の基準深さ
                    if 倒置の直後である:
                        倒置の直後である = False
                        末尾はカナ表現か = False

                if 段階表現[0][1] not in 章の区分と数値の変換表:
                    if 現在の段階表現の基準深さ == -1:
                        未判定の段階表現のdeque.appendleft(段階表現)
                    else:
                        推定は成功か, 推定結果, 深さの推定結果, = self._infer_level(
                            段階表現=段階表現, 現在の深さ=現在の段階表現の基準深さ, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現)
                        if not 推定は成功か:
                            continue
                        段階表現の基準深さ = 深さの推定結果
                        法律名と段階表現の対応表[target_law.name].add(tuple(推定結果))
                else:

                    推定は成功か, 推定結果, 深さの推定結果, = self._infer_level(
                        段階表現=段階表現, 現在の深さ=現在の段階表現の基準深さ, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現)
                    if not 推定は成功か:
                        continue
                    段階表現の基準深さ = 深さの推定結果
                    法律名と段階表現の対応表[target_law.name].add(tuple(推定結果))
                    for 未判定の段階表現 in 未判定の段階表現のdeque:
                        推定は成功か, 推定結果, 深さの推定結果, = self._infer_level(
                            段階表現=段階表現, 現在の深さ=現在の段階表現の基準深さ, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現)
                        if not 推定は成功か:
                            continue
                        段階表現の基準深さ = 深さの推定結果
                        法律名と段階表現の対応表[target_law.name].add(tuple(推定結果))
                    未判定の段階表現のdeque = deque()

                段階表現リストの行番号 -= 1
                if 段階表現リストの行番号 < 0:
                    break

                段階表現のスタート, 段階表現, 倒置表現フラグ = 段階表現のリスト[段階表現リストの行番号]

        self.context.set_data(data=law_dto.name, dto=dto)

        position_list.sort()
        tokens = []
        while cursor.step():

            has_next = True
            while position_list.now_start <= cursor.position <= position_list.now_end:
                tokens.append(cursor.now)
                has_next = cursor.step()
                if not has_next:
                    break
            if not has_next:
                break
            if not position_list.step():
                break
        results.remove_kewywords(tokens)
        for 法律名, 段階表現 in 法律名と段階表現の対応表.items():
            kw = SpecifiedKeyword(headword=法律名, subwords=段階表現, is_force=True)
            results.add_keyword(kw)
        for 法律名 in 法律名の一覧:
            if 法律名 not in 法律名と段階表現の対応表:
                kw = SpecifiedKeyword(
                    headword=法律名, subwords=段階表現, is_force=True)
                results.add_keyword(kw)

        return results

    def _infer_level(self, 段階表現: List[Tuple[str, str]], 現在の深さ, 末尾はカナ表現か, 現在の章表現=None):
        result = (現在の章表現 or [])[:]
        一つ前の深さ = 現在の深さ
        for 番号, 深さ in 段階表現:
            if not 番号.isnumeric():
                if len(番号) > 1:
                    continue
                if 末尾はカナ表現か == True:
                    result.pop()
                result.append(番号)
                末尾はカナ表現か = True

                continue
            一つ前の深さ = 現在の深さ
            現在の深さ = 章の区分と数値の変換表.get(深さ, 現在の深さ + 1)
            if 現在の深さ < 2:
                continue
            if 現在の深さ - 一つ前の深さ > 1:
                return False, False, False
            if 現在の深さ < 一つ前の深さ:
                result = result[:現在の深さ]
            result.append(番号 + 現在の深さ)

        return True, result, 現在の深さ

    def _set_law_positions(self, doc: Doc, law_list: List, lawname, face=''):

        text = doc.text
        _face = face or lawname
        start = text.find(_face)

        while start != -1:
            law_list.append(LawDTO(lawname, start=start, face=face))
            start = text.find(_face, start + 1)

    def _get_hittokens(self, doc: Doc, word: str, tokens: Option[List] = None):
        if tokens is None:
            tokens = []
        is_matched = False
        for token in doc:

            if token.lemma_ not in word and word not in token.lemma_:
                if is_matched:
                    break
                continue
            is_matched = True
            tokens.append(token)

        return tokens

    def _add_law_expressions(self, 法律名, 確定した条文表現のリスト, lawexpessions: Set):

        for waiting_path in 確定した条文表現のリスト:
            is_path_exist = True
            lawexpession = (法律名, ) + tuple(r[1] for r in waiting_path)
            lawexpessions.add(lawexpession)
