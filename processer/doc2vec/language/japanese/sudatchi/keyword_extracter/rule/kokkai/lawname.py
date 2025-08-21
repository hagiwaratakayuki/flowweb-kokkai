

from typing import Any, Deque, Iterator, List, Literal, Optional, Set, Tuple, Union
from sudachipy.morpheme import Morpheme

import numpy as np


from doc2vec.util.specified_keyword import SpecifiedKeyword
import regex as re


import os
import json
from operator import attrgetter, itemgetter
from collections import defaultdict, deque
from data_loader.kokkai import DTO


from doc2vec.spacy.japanese_language.components.keyword_extract.rule.kokkai.discussion_context import DiscussionContext
from doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from doc2vec.language.japanese.sudatchi.util.matcher.preset import number


startkey = attrgetter('start')
zerogetter = itemgetter(0)

章としての区分を表す単語 = r"編章条項節款目"
区分の最大深さ = len(章としての区分を表す単語) - 1
カナ区分の深さ = 区分の最大深さ + 1

章区分を表すパターンと分割パターンのペアのリスト = [
    (re.compile(r'(第?\d[' + 章としての区分を表す単語 + r'の、]*)+\p{Katakana}*'),
     re.compile(r'(\d+|\p{Katakana}+)([' + 章としての区分を表す単語 + r'、]?)'),)

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

並列を表す接続詞 = {
    'と', '並び', '及び',
}


DUMMY_SET = {0}


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


Kana = set(['イ', 'ロ', 'ハ', 'ニ', 'ホ', 'ヘ', 'ト', 'チ', 'リ', 'ヌ', 'ル', 'ヲ', 'ワ', 'カ', 'ヨ', 'タ', 'レ', 'ソ', 'ツ', 'ネ', 'ナ', 'ラ', 'ム',
           'ウ', 'ヰ', 'ノ', 'オ', 'ク', 'ヤ', 'マ', 'ケ', 'フ', 'コ', 'エ', 'テ', 'ア', 'サ', 'キ', 'ユ', 'メ', 'ミ', 'シ', 'ヱ', 'ヒ', 'モ', 'セ', 'ス', 'ン'])


class ChapterExtracter:
    token_limit: int
    index: int
    tokens: List[Morpheme]

    def __init__(self, parse_result: SudatchiDTO):
        self.token_limit = len(parse_result.tokens)
        self.index = 0
        self.tokens = parse_result.tokens

    def exec(self, start, end, law_start, law_end, tokens: Set) -> Union[Literal[False], List]:
        depth = 0
        is_relative = True
        result = ChapterExpression()
        results = [result]
        is_guass = True

        while self.index < self.token_limit:
            token = self.tokens[self.index]
            self.index + 1
            if law_start <= token.begin() < law_end:
                tokens.add(token)
                continue

            if token.end() <= start:
                continue
            if token.end() >= end:
                break
            if number.matcher(token) == True:
                self.index + 1
                if self.index < self.token_limit:
                    target_token = self.tokens[self.index]

                    target_depth = 章の区分と数値の変換表.get(
                        target_token.surface(), None)
                    if target_depth == None:
                        back_index = self.index - 2
                        if back_index > 0:
                            back_token = self.tokens[back_index]
                        if back_token.surface() == 'の':
                            depth + 1
                            result.append((token.normalized_form(), depth,))
                        if back_token.surface() == '、':
                            back_index -= 1

                            if back_index < 0:
                                continue

                            back_token = self.tokens[back_index]
                            if back_token.surface() == 'の':
                                depth + 1
                                result.append(
                                    (token.normalized_form(), depth,))
                            if number.matcher(back_token) or token.normalized_form() in 並列を表す接続詞:
                                pass
                                # result.append
                        continue

                    if target_depth < 2:
                        continue
                    if target_depth <= depth:
                        expressions = [
                            exp[0] for exp in result.expressions if exp[1] > target_depth]
                        result = ChapterExpression(
                            expressions=expressions, is_relative=False)
                        results.append(result)
                    depth = target_depth
                    result.append(token.normalized_form(), depth=depth,
                                  chapter_word=target_token.surface())
                    tokens.add(token)
        len_results = len(results)
        if len_results == 1 and len(result.expressions) == 0:
            return False

        return results


class ChapterExpression:
    is_relative: bool
    expressions: List[Tuple[str, int, Optional[str]]]
    is_reverse: bool
    base_depth: int

    def __init__(self, expressions=[], base_depth=0, is_relative=False, is_reverse=True):
        self.expressions = expressions
        self.base_depth = base_depth
        self.is_relative = is_relative
        self.is_reverse = is_reverse

    def append(self, chapter_count: str, depth: int, chapter_word: Optional[str] = None):
        self.expressions.append((chapter_count, depth, chapter_word))


class LawDTO:
    _start: int
    is_reverse: bool
    face: str
    name: str
    is_guass: bool
    end: int
    chapter_expressions: List[ChapterExpression]

    def __init__(self, name, start, face=None, is_guass=False):
        self.name = name
        self.start = start

        self.is_reverse = False
        if face != None:
            _face = face
        else:
            _face = name

        self.end = start + len(_face)
        self.is_guass = is_guass
        self.chapter_expressions = []

    def add_chapteer_expression(self, chapter_expression):
        self.chapter_expressions.append(chapter_expression)


class LawDTOList:
    sequence: List[LawDTO]
    index: int

    now: LawDTO
    next: LawDTO
    count: bool

    def __init__(self):
        self.sequence = []
        self.is_exist = False

    def append(self, dto: LawDTO):
        self.sequence.append(dto)
        self.count += 1

    def prepend(self, dto: LawDTO):
        self.sequence.insert(0, dto)
        self.count += 1

    def prepare(self):
        self.sequence.sort(key=startkey)

        return self.reset_index()

    def get_first(self) -> Union[False, LawDTO]:
        if self.count == 0:
            return False
        return self.sequence[0]

    def reset_index(self):
        self.index = -1

    def step(self) -> bool:

        self.index += 1
        diff = self.count - self.index
        if diff <= 0:

            return False
        self.now = self.sequence[self.index]
        if diff == -1:

            self.next = None
        else:
            self.next = self.sequence[self.index + 1]

        dto = self.sequence[self.index]

        self.now = dto
        return True


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

    def execute(self, parse_result: SudatchiDTO, document_vector, sentiment_results, dto: DTO, results: ExtractResultDTO, indexer: Any):

        position_list = PositionList()
        reverse_dict = defaultdict(set)
        sent_number = -1
        all_text = dto.get_text()
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
                headword=detected_phrase, is_force=True, source_ids={1}))

        if law_count == standard_phrase_count:
            return results
        商売の方法または金商法の略称の一部としての商法である = False

        target_tokens = deque()

        sent_number += 1

        canditates_set = set()
        ryakusyou_canditates_set = set()
        law_dto_list = LawDTOList()
        アイヌ新法が含まれるか = アイヌ新法 in all_text

        if アイヌ新法が含まれるか is True:
            if dto.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称

            start_positions = self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=アイヌ新法の正式名称, face=アイヌ新法)

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
                all_text, law_dto_list=law_dto_list, lawname=活火山法の正式名称, face=活火山法の略称)

            self._get_hittokens(prase_result=parse_result, face=活火山法の略称,
                                tokens=target_tokens, start_positions=start_positions)
        改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in all_text
        改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in all_text

        if 改正前の活火山法の正式名称が存在する:
            additional_law_words.add(活火山法)

            start_positions = self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=改正前の活火山法の正式名称)

        if 改正後の活火山法の正式名称が存在する:

            additional_law_words.add(活火山法)
            start_positions = self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=改正後の活火山法の正式名称)

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
                all_text, law_dto_list=law_dto_list, lawname=法律名)
            self._get_hittokens(parse_result=parse_result, face=法律名,
                                tokens=target_tokens, start_positions=start_positions)

        for 法律名の略称 in 法律名の略称のリスト:
            法律の正式名称 = 略称と正式名称の対応表[法律名の略称]
            self._set_law_positions(
                text=all_text, law_dto_list=law_dto_list, lawname=法律の正式名称, face=法律名の略称)

        # line_laws.extend((m.group(0), m.start(), section_rank[m.group(1)], )
        #             )

        if law_dto_list.count == 0:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if not is_context_exist:
                return results
            law_dto = LawDTO(name=法律名, start=0, face='', is_guass=True)
            law_dto_list.append(law_dto)

            law_list_len = 1
        law_dto_list.prepare()

        first_law = law_dto_list.get_first()
        self.context.set_data(data=law_dto.name, dto=dto)
        if first_law.start > 0:
            psuedo_law_dto = LawDTO(
                name=first_law.name, start=0, face='', is_guass=True)
            law_dto_list.prepend(dto=psuedo_law_dto)

        tokens = set()
        is_in = False
        chapter_extracter = ChapterExtracter(parse_result=parse_result)

        while law_dto_list.step():
            start = law_dto_list.now.start
            if law_dto_list.next == None:
                end = len(all_text)
            else:
                end = law_dto_list.next.start
            chapter_expressions = chapter_extracter.exec(
                start=start, end=end, law_start=law_dto_list.now.start, law_end=law_dto_list.now.end, tokens=tokens)
            if chapter_expressions != False:
                law_dto.chapter_expressions = chapter_expressions
        non_chapter_laws = set()
        law2chapter = defaultdict(set)

        for law_dto in law_dto_list.sequence:
            if not law_dto.chapter_expressions:
                if not law_dto.is_guass:
                    non_chapter_laws.add(law_dto.name)
                continue

            for chapter_expression_dto in law_dto.chapter_expressions:
                expression = tuple(
                    [expression[0] + expression[2] or '' for expression in chapter_expression_dto.expressions])
                law2chapter[law_dto.name].add(expression)
        results.remove_kewywords(tokens)

        for law_name in non_chapter_laws:
            kw = SpecifiedKeyword(
                headword=law_name, source_ids=DUMMY_SET, is_force=True)
            results.add_keyword(kw)
        for law_name, expression_set in law2chapter:
            for expression in expression_set:
                kw = SpecifiedKeyword(
                    headword=law_name, subwords=expression, source_ids=DUMMY_SET, is_force=True)
                results.add_keyword(kw)
        for additional_law_word in additional_law_words:
            kw = SpecifiedKeyword(
                headword=additional_law_word, source_ids=DUMMY_SET, is_force=True)
            results.add_keyword(kw)

        return results
