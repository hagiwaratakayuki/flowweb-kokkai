

from typing import Any, Deque, Iterator, List, Optional, Set, Tuple


import numpy as np


from doc2vec.util.specified_keyword import SpecifiedKeyword
import regex as re


import os
import json
from operator import attrgetter, itemgetter, methodcaller
from collections import defaultdict, deque
from data_loader.kokkai import DTO
from doc2vec.base.protocol.sentiment import SentimentResult

from doc2vec.spacy.japanese_language.components.keyword_extract.rule.kokkai.discussion_context import DiscussionContext
from processor.doc2vec.base.protocol.keyword_extractor import ExtractResultDTO, KeywordExtractRule
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO


startkey = methodcaller('start')
zerogetter = itemgetter(0)

章としての区分を表す単語 = r"編章条項節款目"
区分の最大深さ = len(章としての区分を表す単語) - 1
カナ区分の深さ = 区分の最大深さ + 1

章区分を表すパターンと分割パターンのペアのリスト = [
    (re.compile(r'(第?\d[' + 章としての区分を表す単語 + r'の、]*)+\p{Katakana}*'),
     re.compile(r'(\d+|の、?\p{Katakana}+)([' + 章としての区分を表す単語 + r'、]?)'),)

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


class LawDTO:
    _start: int
    is_reverse: bool
    face: str
    name: str
    _end: int

    def __init__(self, name, start, face=''):
        self.name = name
        self._start = start
        self.face = face
        self.is_reverse = False
        self.len = len(self.get_face())
        self._end = self.start() + self.len

    def start(self):
        return self._start

    def end(self):
        return self._end

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

    def prepare(self):
        self.positions.sort(key=zerogetter)
        self.limit = len(self.positions) - 1
        return self.step()

    def step(self):

        self.index += 1
        if self.limit < self.index:

            return False
        start, end = self.positions[self.index]
        self.now_start = start
        self.now_end = end
        return True


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, parse_result: SudatchiDTO, document_vector, sentiment_results, dto: DTO, results: ExtractResultDTO, postprocessor: Any):

        law_index = defaultdict(set)
        reverse_dict = defaultdict(set)
        sent_number = -1
        all_text = dto.get_text()
        law_count = all_text.count('法')
        needle_words = []
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

        sent_number += 1

        canditates_set = set()
        ryakusyou_canditates_set = set()
        law_list: List[LawDTO] = []
        アイヌ新法が含まれるか = アイヌ新法 in all_text

        if アイヌ新法が含まれるか is True:
            if dto.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称

            start_positions = self._set_law_positions(
                all_text, law_list=law_list, lawname=アイヌ新法の正式名称, face=アイヌ新法)

            self._get_hittokens(parse_result=parse_result, face=アイヌ新法, start_positions=start_positions,
                                tokens=target_tokens)

        活火山法の検索結果 = 活火山法の略称候補.search(all_text)
        活火山法が含まれるか = 活火山法の検索結果 is not None
        if 活火山法が含まれるか is True:
            additional_law_words.add(活火山法)
            活火山法の略称 = 活火山法の検索結果.group(0)
            if dto.published >= "1973-7-13":
                活火山法の正式名称 = 改正後の活火山法の正式名称
            else:
                活火山法の正式名称 = 改正前の活火山法の正式名称
            start_positions = self._set_law_positions(
                all_text, law_list=law_list, lawname=活火山法の正式名称, face=活火山法の略称)

            self._get_hittokens(prase_result=parse_result, face=活火山法の略称,
                                tokens=target_tokens, start_positions=start_positions)
        改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in all_text
        改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in all_text

        if 改正前の活火山法の正式名称が存在する:
            additional_law_words.add(活火山法)

            start_positions = self._set_law_positions(
                all_text, law_list=law_list, lawname=改正前の活火山法の正式名称)
            self._get_hittokens(parse_result=parse_result, face=改正前の活火山法の正式名称, start_positions=start_positions,
                                tokens=target_tokens)
        if 改正後の活火山法の正式名称が存在する:

            additional_law_words.add(活火山法)
            start_positions = self._set_law_positions(
                all_text, law_list=law_list, lawname=改正後の活火山法の正式名称)
            self._get_hittokens(
                parse_result=parse_result, face=改正後の活火山法の正式名称, tokens=target_tokens, start_positions=start_positions)

        for i in range(len(all_text) - 1):
            gram = all_text[i:i + 2]
            canditates_set.update(name_index.get(gram, []))

            ryakusyou_canditates_set.update(
                ryakusyou_tench.get(gram, []))

        略称の可能性があるもののリスト = [
            canditate for canditate in ryakusyou_canditates_set if canditate in all_text]

        ryakusyou_index = [EqInShorter(ry) for ry in 略称の可能性があるもののリスト]
        発見された正式名称のリスト = [
            canditate for canditate in canditates_set if canditate in all_text and canditate not in ryakusyou_index]

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
                all_text) is not None

        for 法律名 in 発見された正式名称のリスト:
            start_positions = self._set_law_positions(
                all_text, law_list=law_list, lawname=法律名)
            self._get_hittokens(parse_result=parse_result, face=法律名,
                                tokens=target_tokens, start_positions=start_positions)

        for 法律名の略称 in 法律名の略称のリスト:
            法律の正式名称 = 略称と正式名称の対応表[法律名の略称]
            start_positions = self._set_law_positions(
                text=all_text, law_list=law_list, lawname=法律の正式名称, face=法律名の略称)
            self._get_hittokens(parse_result=parse_result, face=法律名の略称,
                                tokens=target_tokens, start_positions=start_positions)

        # line_laws.extend((m.group(0), m.start(), section_rank[m.group(1)], )
        #             )

        law_list.sort(key=startkey)

        law_list_len = len(law_list)

        is_context_added = False
        position_list = PositionList()
        if law_list_len == 0:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if not is_context_exist:
                return results
            law_dto = LawDTO(name=法律名, start=0)
            law_list.append(law_dto)
            position_list.append_position(law_dto.start(), law_dto.end())
            is_context_added = True
            law_list_len = 1
        else:
            for law_dto in law_list:
                position_list.append_position(law_dto.start(), law_dto.end())

        段階表現のリスト = []

        段階表現と位置のインデックス = {}

        index = 0
        倒置表現の可能性がある限界 = len(all_text) - 2

        for パターン, 分割パターン in 章区分を表すパターンと分割パターンのペアのリスト:
            for match in パターン.finditer(all_text):
                all_match = match.group(0)

                倒置表現である = False

                if all_match[-1] == 'の':

                    match_end = match.end()

                    if match_end > 倒置表現の可能性がある限界 or all_text[match_end + 1] != '、' or 数字と第を表すパターン.search(all_text[match_end + 1]) == None:
                        倒置表現である = False
                    else:
                        倒置表現である = True
                段階表現のリスト.append(
                    (match.start(), 分割パターン.findall(all_text), 倒置表現である, ))
                段階表現と位置のインデックス[match.start()] = index
                position_list.append_position(match.start(), match.end())

        法律名のインデックス = -1
        for law_dto in law_list:
            法律名のインデックス += 1
            next_position = law_dto.start() + law_dto.len
            リンクしている段階表現のID = 段階表現と位置のインデックス.get(next_position)
            if リンクしている段階表現のID is not None:

                law_dto.is_reverse = 段階表現のリスト[リンクしている段階表現のID][2]

            elif all_text[next_position] in 連続章段階表現の接続語:  # 『憲法の、第9条』と『9条ですね、憲法の』、みたいな倒置表現
                リンクしている段階表現のID = 段階表現と位置のインデックス.get(
                    next_position + 1) or 段階表現と位置のインデックス.get(next_position + 2) or 段階表現と位置のインデックス.get(next_position + 3)
                if リンクしている段階表現のID is not None:
                    law_dto.is_reverse = 段階表現のリスト[リンクしている段階表現のID][2]
                else:

                    law_dto.is_reverse = all_text[next_position] == 'の'

        law_dto = law_list[0]
        if not is_context_added:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if is_context_exist and 法律名 != None and law_dto.name != 法律名 and law_dto.start() != 0:
                law_dto = LawDTO(name=法律名, start=0)
                law_list.insert(0, law_dto)
                law_list_len += 1
        法律名と段階表現の対応表, 法律名の一覧 = self.段階表現の抽出(
            段階表現のリスト=段階表現のリスト, law_list_len=law_list_len, law_list=law_list)

        self.context.set_data(data=law_list[-1].name, dto=dto)
        is_positions_exist = position_list.prepare()
        if not is_positions_exist:
            return results

        tokens = set()
        is_in = False
        position = 0

        for token in parse_result.tokens:

            if position_list.now_start <= token.begin() <= position_list.now_end:
                is_in = True

                tokens.add(token)
            elif is_in:
                is_in = False
                if not position_list.step():
                    break

        results.remove_kewywords(tokens)

        for 法律名, 対応した段階表現のリスト in 法律名と段階表現の対応表.items():
            for 対応した段階表現 in 対応した段階表現のリスト:
                kw = SpecifiedKeyword(
                    headword=法律名, subwords=対応した段階表現, tokens=DUMMY_SET, is_force=True)
            results.add_keyword(kw)
        for 法律名 in 法律名の一覧:
            if 法律名 not in 法律名と段階表現の対応表:
                kw = SpecifiedKeyword(
                    headword=法律名, tokens=DUMMY_SET, is_force=True)

                results.add_keyword(kw)
        for additional_law_word in additional_law_words:
            kw = SpecifiedKeyword(
                headword=additional_law_word, tokens=DUMMY_SET, is_force=True)
            results.add_keyword(kw)

        return results

    def 段階表現の抽出(self, 段階表現のリスト, law_list_len, law_list: List[LawDTO]):
        段階表現のリストの長さ = len(段階表現のリスト)
        if 段階表現のリストの長さ == 0:
            return {}, {law_dto.name for law_dto in law_list}
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
            law_dto: LawDTO = law_list[law_list_index]
            法律名の一覧.add(law_dto.name)
            law_list_index -= 1

            is_tail = True

            while 段階表現のスタート > law_dto.start():

                if is_tail == True:
                    is_tail = False
                    if prev_law_dto != None and prev_law_dto.is_reverse:
                        target_law = prev_law_dto
                        現在の段階表現の基準深さ = 以前の段階表現の基準深さ
                        倒置の直後である = True

                    else:
                        target_law = law_dto
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
                        推定は成功か, 推定される現在の章表現, 末尾はカナ表現か = self._infer_level(
                            段階表現=段階表現, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現, 法律名と段階表現の対応表=法律名と段階表現の対応表, 現在の法律名=target_law.name)
                        if 推定は成功か:
                            現在の章表現 = 推定される現在の章表現

                else:

                    推定は成功か, 推定される現在の章表現, 末尾はカナ表現か = self._infer_level(
                        段階表現=段階表現, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現, 法律名と段階表現の対応表=法律名と段階表現の対応表, 現在の法律名=target_law.name)
                    if 推定は成功か:

                        現在の章表現 = 推定される現在の章表現
                        for 未判定の段階表現 in 未判定の段階表現のdeque:
                            推定は成功か, 推定される現在の章表現, 末尾はカナ表現か = self._infer_level(
                                段階表現=段階表現, 現在の数値深さ=現在の段階表現の基準深さ, 末尾はカナ表現か=末尾はカナ表現か, 現在の章表現=現在の章表現, 法律名と段階表現の対応表=法律名と段階表現の対応表, 現在の法律名=target_law.name)
                            if not 推定は成功か:
                                continue

                            現在の章表現 = 推定される現在の章表現

                        未判定の段階表現のdeque = deque()

                段階表現リストの行番号 -= 1
                if 段階表現リストの行番号 < 0:
                    break

                段階表現のスタート, 段階表現, 倒置表現フラグ = 段階表現のリスト[段階表現リストの行番号]
        return 法律名と段階表現の対応表, 法律名の一覧

    def _infer_level(self, 段階表現: List[Tuple[str, str]], 末尾はカナ表現か, 現在の章表現=None, 法律名と段階表現の対応表={}, 現在の法律名=''):

        result = list(現在の章表現 or [])

        if 現在の章表現 != None:
            現在の数値深さ = result[-1][1]
        else:
            現在の数値深さ = -1

        results = [result]
        一つ前の深さ = 現在の数値深さ
        is_first = True
        for 番号, 深さ in 段階表現:

            if not 番号.isnumeric():
                if len(番号) > 1:
                    continue
                if 末尾はカナ表現か == True:
                    result.pop()
                result.append((番号, カナ区分の深さ,))
                末尾はカナ表現か = True

                continue
            一つ前の深さ = 現在の数値深さ
            現在の数値深さ = 章の区分と数値の変換表.get(深さ, 現在の数値深さ + 1)

            if 現在の数値深さ < 2:
                continue
            if 一つ前の深さ > -1 and 現在の数値深さ - 一つ前の深さ > 1:

                return False, False, 末尾はカナ表現か

            if 現在の数値深さ <= 一つ前の深さ:

                next_result = []

                for 条文表現, 数値深さ in result:

                    if 数値深さ < 現在の数値深さ:

                        next_result.append((条文表現, 数値深さ,))

                result = next_result
                if is_first:
                    results[0] = result
                else:
                    results.append(result)
            if is_first:
                is_first = False
            result.append((番号 + 深さ, 現在の数値深さ,))
        for result in results:
            法律名と段階表現の対応表[現在の法律名].add(tuple([row[0] for row in result]))
        if not results:
            現在の章表現 = []
        else:
            現在の章表現 = results[-1]
        return True, 現在の章表現, 末尾はカナ表現か

    def _set_law_positions(self, text, law_list: List, lawname, face=''):

        _face = face or lawname
        start = text.find(_face)
        law_result = []

        while start != -1:
            law_result.append(start)
            law_list.append(LawDTO(lawname, start=start, face=face))
            start = text.find(_face, start + 1)
        return law_result

    def _get_hittokens(self, parse_result: SudatchiDTO, face: str, start_positions: List[int], tokens: Optional[List] = None):
        if tokens is None:
            tokens = []
        limit_index = len(start_positions)
        start_index = 0
        distance = len(face)
        start_position = start_positions[start_index]
        end_position = start_position + distance
        for token in parse_result.tokens:

            if token.begin() < start_position:
                continue
            if token.begin() > end_position:
                start_index += 1
                if limit_index <= start_index:
                    break
                start_position = start_positions[start_index]
                end_position = start_position + distance
                continue

            tokens.append(token)

        return tokens

    def _add_law_expressions(self, 法律名, 確定した条文表現のリスト, lawexpessions: Set):

        for waiting_path in 確定した条文表現のリスト:
            is_path_exist = True
            lawexpession = (法律名, ) + tuple(r[1] for r in waiting_path)
            lawexpessions.add(lawexpession)
