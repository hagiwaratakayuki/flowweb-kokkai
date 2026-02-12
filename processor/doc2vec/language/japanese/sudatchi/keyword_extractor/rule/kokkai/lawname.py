

import math

from tracemalloc import start
from turtle import st
from types import NoneType
from typing import Any, Callable, Deque, Iterator, List, Literal, Optional, Set, Tuple, Union

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
from doc2vec.base.protocol.keyword_extractor import ExtractResultDTO, KeywordExtractRule
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from doc2vec.language.japanese.sudatchi.util.matcher.preset import number
from doc2vec.language.japanese.sudatchi.util.matcher.preset import adnominal, comma, counter_word_possible, particle


startkey = attrgetter('start')
zerogetter = itemgetter(0)

章としての区分を表す単語 = r"条項号"
グループ分け単語 = set('編章節款目')
章とグループ分けの単語 = set(章としての区分を表す単語) | グループ分け単語

区分の最大深さ = len(章としての区分を表す単語) - 1
カナ区分の深さ = 区分の最大深さ + 1


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


DUMMY_SET = {0}


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


カタカナ一文字 = {'イ', 'ロ', 'ハ', 'ニ', 'ホ', 'ヘ', 'ト', 'チ', 'リ', 'ヌ', 'ル', 'ヲ', 'ワ', 'カ', 'ヨ', 'タ', 'レ', 'ソ', 'ツ', 'ネ', 'ナ', 'ラ', 'ム',
           'ウ', 'ヰ', 'ノ', 'オ', 'ク', 'ヤ', 'マ', 'ケ', 'フ', 'コ', 'エ', 'テ', 'ア', 'サ', 'キ', 'ユ', 'メ', 'ミ', 'シ', 'ヱ', 'ヒ', 'モ', 'セ', 'ス', 'ン'}


parallel_expressions = {
    '並び',
    'ならび',
    'および',
    '及び',
    'ないし',
    '乃至',
    '又',
    'また',
    '亦',
    '復',
    '股',  # 誤記対策
    '叉',
    'あるいは'
    'と'

}
parallel_particles = {'や', 'と', 'か'}


イロハ表記につながる単語 = {'の', 章としての区分を表す単語[-1]}


class ChapterExpressionElement:
    depth: int
    chapter_number: str
    chapter_word: Optional[str]

    def __init__(self, chapter_number, chapter_word, depth):
        self.depth = depth
        self.chapter_number = chapter_number
        self.chapter_word = chapter_word


ExpressionListType = List[ChapterExpressionElement]


class ChapterExpression:
    is_relative: bool
    elements: ExpressionListType
    is_reverse: bool
    depth: int

    def __init__(self, elements=[], is_relative=False, is_reverse=False, depth=None):

        self.elements = elements[:]

        self.is_relative = is_relative
        self.is_reverse = is_reverse
        if depth != None:
            self.depth = depth
        else:
            self.depth = len(elements) - 1

    def append(self, chapter_number: str, chapter_word: Optional[str] = None):

        self.elements.append(ChapterExpressionElement(
            chapter_number, chapter_word, self.depth))
        self.depth += 1

    def get_tuple_expression(self, base_element_strs: Tuple[str, ...]):

        result_expression = []
        start_depth = 0
        if self.depth == 0:
            return False
        if self.is_relative:
            start_depth = -1
            expression_index = -1

            for element in self.elements:
                expression_index += 1
                depth = 章の区分と数値の変換表.get(element.chapter_word)
                if depth != None:
                    start_depth = depth - expression_index
                    break
            if start_depth == -1:
                start_depth = math.max(
                    0, len(base_element_strs) - len(self.elements))
            if base_element_strs and base_element_strs[-1] in カタカナ一文字 and self.elements[-1].chapter_word not in カタカナ一文字:
                start_depth = math.max(0, start_depth - 1)

            result_expression.extend(base_element_strs[:start_depth])

        depth = start_depth
        for element in self.elements:

            chapter_string = element.chapter_number

            if not element.chapter_word:
                if depth < 3:
                    chapter_string += 章としての区分を表す単語[depth]
            else:
                chapter_string += element.chapter_word

            result_expression.append(chapter_string)
            depth += 1

        return tuple(result_expression)


class ChapterExpressionList:
    sequence: List[ChapterExpression]
    cursor_head: Optional[ChapterExpression]

    def __init__(self):
        self.sequence = []
        self.cursor_head = None

    def add_element(self, chapter_number, chapter_word: Optional[str] = None, depth=None):

        if self.cursor_head == None:
            expression = self.add_new_expression(
                is_relative=depth != None and depth != 0, depth=depth)
            expression.append(chapter_number=chapter_number,
                              chapter_word=chapter_word)
            return

        elif depth != None:
            if self.cursor_head.is_relative:
                if self.cursor_head.depth != depth - 1:
                    self.add_new_expression(
                        is_relative=depth != 0)
            elif depth < self.cursor_head.depth:

                elements = [
                    element for element in self.cursor_head.elements if element.depth < depth]

                self.add_new_expression(
                    elements=elements)

        self.cursor_head.append(chapter_number=chapter_number,
                                chapter_word=chapter_word)

    def add_new_expression(self, elements=[], is_relative=False, depth=None):
        expression = ChapterExpression(
            elements=elements, is_relative=is_relative, depth=depth)
        self.sequence.append(expression)
        self.cursor_head = expression
        return expression

    def get_expression_tuples(self):
        results = []

        # limit = len(self.sequence)
        # index = 0
        base_elements = []
        is_exist = False

        for target in self.sequence:

            if target.is_relative:
                elements = target.get_tuple_expression(
                    base_element_strs=base_elements)

            else:
                elements = target.get_tuple_expression(base_element_strs=[])
            if elements == False:
                continue
            is_exist = True
            results.append(elements)
            base_elements = elements
        if not is_exist:
            return False
        return results

    def イロハの追加(self, イロハ表記: str):
        if self.cursor_head == None:
            self.add_new_expression(is_relative=True)
            self.add_element(chapter_number=イロハ表記)

        elif self.cursor_head.depth >= 2:
            self.add_element(chapter_number=イロハ表記, depth=3)
        else:
            if self.cursor_head.depth == -1:
                elements = []
            elif self.cursor_head.elements[-1] in カタカナ一文字:
                elements = self.cursor_head.elements[:-1]
            else:
                elements = self.cursor_head.elements[:]
            self.add_new_expression(is_relative=True, elements=elements)
            self.cursor_head.append(chapter_number=イロハ表記)

    def is_exist(self):
        self.cursor_head != None


class TokenCursor:
    tokens: List[Morpheme]
    limit: int
    index: int
    token: Optional[Morpheme]

    def __init__(self, tokens: List[Morpheme], index=-1):

        self.tokens = tokens

        self.limit = len(tokens)
        self.index = index
        if -1 < self.index < self.limit:
            self.token = self.tokens[index]

        else:
            self.token = None

    def step(self):
        self.index += 1
        if self.limit > self.index:
            self.token = self.tokens[self.index]

            return True
        return False

    def get_back(self):
        if self.index < 1:
            return False

        return TokenCursor(tokens=self.tokens, index=self.index - 1)

    def get_next(self, is_step=False):
        next_index = self.index + 1

        if next_index >= self.limit:
            return False
        if is_step:
            self.index = next_index
            self.token = self.tokens[self.index]

        return TokenCursor(tokens=self.tokens, index=next_index)


class ChapterExtractor:
    cursor: TokenCursor
    all_text: str

    def __init__(self, parse_result: SudatchiDTO, all_text: str):
        self.token_limit = len(parse_result.tokens)
        self.cursor = TokenCursor(tokens=parse_result.tokens)

        self.all_text = all_text

    def exec(self, start, end, law_start, law_end, tokens: Set) -> Union[Literal[False], ChapterExpressionList]:

        law_indexs = set()

        chapter_expressions = ChapterExpressionList()

        while self.cursor.step():
            is_parallel = False
            token = self.cursor.token

            if token.end() <= start:

                continue
            if law_start <= token.begin() < law_end:
                law_indexs.add(self.cursor.index)

                tokens.add(token)

                continue
            if token.end() == end:
                break

            if token.end() > end:
                self.cursor.index -= 1
                break

            if number.matcher(token) == True:

                next_step_cursor = self.cursor.get_next()

                if next_step_cursor != False:

                    next_token = next_step_cursor.token

                    chapter_word_candiate = next_token.surface()

                    if chapter_word_candiate in グループ分け単語:

                        continue

                    target_depth = 章の区分と数値の変換表.get(
                        chapter_word_candiate, None)

                    if target_depth != None:

                        tokens.add(token)
                        tokens.add(next_token)

                        chapter_expressions.add_element(depth=target_depth, chapter_number=token.normalized_form(
                        ), chapter_word=chapter_word_candiate)

                    else:

                        if counter_word_possible.matcher(next_token):

                            continue

                        back_cursor = self.cursor.get_back()
                        is_step_expression = False
                        is_new_expression = False

                        if back_cursor == False:
                            is_step_expression = start == 0

                        else:

                            if comma.matcher(back_cursor.token):

                                back_cursor = back_cursor.get_back()
                                if back_cursor == False:
                                    continue

                                if number.matcher(back_cursor.token) or back_cursor.token.surface() in 章の区分と数値の変換表:
                                    is_step_expression = True
                                    is_new_expression = True

                            if back_cursor.index in law_indexs:

                                is_step_expression = True

                            if not is_step_expression:
                                if adnominal.matcher(back_cursor.token):
                                    is_step_expression = True
                                    is_new_expression = True

                                elif back_cursor.token.surface() == 'の':
                                    next_back_cursor = back_cursor.get_back()
                                    if number.matcher(next_back_cursor.token) or next_back_cursor.token.surface() in 章とグループ分けの単語:
                                        is_step_expression = True
                                else:
                                    _is_parallel, is_particle, critetion_cursor = self._check_parallel(
                                        back_cursor)
                                    if _is_parallel == True:

                                        next_back_cursor = critetion_cursor.get_back()
                                        if comma.matcher(next_back_cursor.token):
                                            next_back_cursor = next_back_cursor.get_back()
                                        if number.matcher(next_back_cursor.token) or next_back_cursor.token.surface() in 章とグループ分けの単語:
                                            is_step_expression = True
                                            is_new_expression = True
                                    else:
                                        if is_particle:

                                            is_step_expression = True
                                            back_cursor = back_cursor.get_back()

                        if is_step_expression:

                            tokens.add(token)
                            if is_new_expression:
                                chapter_expressions.add_new_expression(
                                    is_relative=True)

                            chapter_expressions.add_element(
                                chapter_number=token.normalized_form())

                        continue

            if token.surface() in カタカナ一文字:
                is_chapter = chapter_expressions.cursor_head != None and chapter_expressions.cursor_head.depth >= 2
                if not is_chapter:
                    back_cursor = self.cursor.get_back()
                    if back_cursor != False:

                        if self._イロハ表記に繋がるか判定する関数(back_cursor.token.surface()):
                            is_chapter = True
                        elif comma.matcher(back_cursor.token):
                            next_back_cursor = back_cursor.get_back()
                            is_chapter = next_back_cursor != False and self._イロハ表記に繋がるか判定する関数(
                                next_back_cursor.token)

                if is_chapter:
                    chapter_expressions.イロハの追加(token.surface())

        if chapter_expressions.cursor_head == None:
            return False

        return chapter_expressions

    def _イロハ表記に繋がるか判定する関数(self, token: Morpheme):
        return token.surface() in イロハ表記につながる単語 or number.matcher(token)

    def _check_parallel(self, cursor: TokenCursor) -> Union[Tuple[Literal[True], bool, TokenCursor], Tuple[Literal[False], bool, NoneType]]:
        is_particle = particle.matcher(cursor.token)
        if is_particle == True:
            if cursor.token.normalized_form() in parallel_particles:
                back_cursor = cursor.get_back()
                if back_cursor == False:
                    return False, is_particle, None
                if back_cursor.token.surface() in parallel_expressions:
                    return True, particle.matcher(back_cursor.token), back_cursor
                return True, is_particle, cursor
            back_cursor = cursor.get_back()
            if back_cursor.token.surface() in parallel_expressions:
                return True, is_particle, back_cursor
        else:
            if cursor.token in parallel_expressions:
                return True, is_particle, cursor
            return False, is_particle, None
        return False, False, None


class LawDTO:
    start: int
    is_reverse: bool
    face: str
    name: str
    is_guass: bool
    end: Optional[int]
    chapter_expressions: Union[Literal[False], ChapterExpressionList]

    def __init__(self, name: str, start=None, face=None, is_guass=False):

        self.name = name
        self.start = start

        self.is_reverse = False

        _face = face or name
        if is_guass == False:
            self.end = start + len(_face)
        else:
            self.end = 0
            self.start = 0

        self.is_guass = is_guass
        self.face = _face
        self.chapter_expressions = False


class LawDTOList:
    sequence: List[LawDTO]
    index: int

    now: LawDTO
    next: LawDTO
    count: bool

    def __init__(self):
        self.sequence = []
        self.is_exist = False
        self.count = 0

    def append(self, dto: LawDTO):
        self.sequence.append(dto)
        self.count += 1

    def prepend(self, dto: LawDTO):
        self.sequence.insert(0, dto)
        self.count += 1

    def prepare(self):
        self.sequence.sort(key=startkey)

        return self.reset_index()

    def get_last(self) -> Union[Literal[False], LawDTO]:
        if self.count == 0:
            return False
        return self.sequence[-1]

    def get_first(self):
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

        if diff == 1:

            self.next = None
        else:
            self.next = self.sequence[self.index + 1]

        dto = self.sequence[self.index]

        self.now = dto
        return True


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, parse_result: SudatchiDTO, document_vector, sentiment_results, dto: DTO, results: ExtractResultDTO, postprocessor: Any):

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
                headword=detected_phrase, is_force=True, tokens={1}))

        if law_count != 0 and law_count == standard_phrase_count:
            return results

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

            self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=アイヌ新法の正式名称, face=アイヌ新法)

        活火山法の検索結果 = 活火山法の略称候補.search(all_text)
        活火山法が含まれるか = 活火山法の検索結果 is not None
        if 活火山法が含まれるか is True:
            additional_law_words.add(活火山法)
            活火山法の略称 = 活火山法の検索結果.group(0)
            if dto.published >= "1973-7-13":
                活火山法の正式名称 = 改正後の活火山法の正式名称
            else:
                活火山法の正式名称 = 改正前の活火山法の正式名称
            self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=活火山法の正式名称, face=活火山法の略称)

        改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in all_text
        改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in all_text

        if 改正前の活火山法の正式名称が存在する:
            additional_law_words.add(活火山法)

            self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=改正前の活火山法の正式名称)

        if 改正後の活火山法の正式名称が存在する:

            additional_law_words.add(活火山法)
            self._set_law_positions(
                all_text, law_dto_list=law_dto_list, lawname=改正後の活火山法の正式名称)

        for i in range(len(all_text) - 1):
            gram = all_text[i:i + 2]
            canditates_set.update(name_index.get(gram, []))

            ryakusyou_canditates_set.update(
                ryakusyou_tench.get(gram, []))

        略称の可能性があるもののリスト = [
            canditate for canditate in ryakusyou_canditates_set if canditate in all_text]

        ryakusyou_index = [EqInShorter(ry) for ry in 略称の可能性があるもののリスト]
        発見された正式名称の一覧 = {
            canditate for canditate in canditates_set if canditate in all_text and canditate not in ryakusyou_index}

        正式名称のインデックス = [EqInShorter(正式名称)
                       for 正式名称 in 発見された正式名称の一覧]

        法律名の略称のリスト = [
            canditate for canditate in 略称の可能性があるもののリスト if canditate not in 正式名称のインデックス]
        for 法律名の略称 in 法律名の略称のリスト:
            if 法律名の略称 == アイヌ新法 or 法律名の略称 == 活火山法:
                continue

            reverse_dict[略称と正式名称の対応表[法律名の略称]].add(法律名の略称)

        for 法律名 in 発見された正式名称の一覧:
            if 法律名 == '商法':

                self._set_law_positions(
                    all_text, law_dto_list=law_dto_list, lawname=法律名, filter_func=self._法律の略称ではない商法をブロックする関数)
            else:
                self._set_law_positions(
                    all_text, law_dto_list=law_dto_list, lawname=法律名)

        for 法律名の略称 in 法律名の略称のリスト:
            法律の正式名称 = 略称と正式名称の対応表[法律名の略称]

            self._set_law_positions(
                text=all_text, law_dto_list=law_dto_list, lawname=法律の正式名称, face=法律名の略称)

        # 本当に空なのかを判定
        if law_dto_list.count == 0:
            is_context_exist, 法律名 = self.context.get_data(dto=dto)
            if not is_context_exist:

                return results

            law_dto = LawDTO(name=法律名, is_guass=True)
            law_dto_list.append(law_dto)

        law_dto_list.prepare()

        first_law = law_dto_list.get_first()
        if first_law != False and first_law.start > 0:
            is_context_exist, data = self.context.get_data(dto=dto)

            if is_context_exist == True:

                law_name = data
            else:
                law_name = first_law.name

            psuedo_law_dto = LawDTO(
                name=law_name, is_guass=True)

            law_dto_list.prepend(dto=psuedo_law_dto)
        last_law = law_dto_list.get_last()
        if last_law != False:
            self.context.set_data(data=last_law.name, dto=dto)
        tokens = set()

        chapter_extracter = ChapterExtractor(
            parse_result=parse_result, all_text=all_text)

        while law_dto_list.step():

            start = law_dto_list.now.start

            if law_dto_list.next == None:
                end = len(all_text)
            else:
                end = law_dto_list.next.start

            chapter_expressions = chapter_extracter.exec(
                start=start, end=end, law_start=law_dto_list.now.start, law_end=law_dto_list.now.end, tokens=tokens)

            if chapter_expressions != False:

                law_dto_list.now.chapter_expressions = chapter_expressions

        non_chapter_laws = set()
        law2chapter = defaultdict(set)

        for law_dto in law_dto_list.sequence:

            if not law_dto.chapter_expressions:
                if not law_dto.is_guass:

                    non_chapter_laws.add(law_dto.name)
                continue

            expression_tuples = law_dto.chapter_expressions.get_expression_tuples()

            if expression_tuples == False:
                continue

            law2chapter[law_dto.name].update(expression_tuples)

        results.remove_kewywords(tokens)

        for law_name in non_chapter_laws:

            kw = SpecifiedKeyword(
                headword=law_name, tokens=DUMMY_SET, is_force=True)
            results.add_keyword(kw)

        for law_name, expression_set in law2chapter.items():

            for expression_tuple in expression_set:

                kw = SpecifiedKeyword(
                    headword=law_name, subwords=expression_tuple, tokens=DUMMY_SET, is_force=True)
                results.add_keyword(kw, is_overwrite_token=False)
        for additional_law_word in additional_law_words:
            kw = SpecifiedKeyword(
                headword=additional_law_word, tokens=DUMMY_SET, is_force=True)
            results.add_keyword(kw, is_overwrite_token=False)

        return results

    def _set_law_positions(self, text: str, law_dto_list: LawDTOList, lawname, face='', filter_func: Optional[Callable[[str, int], bool]] = None):

        target = face or lawname
        start = text.find(target)

        while start != -1:

            if filter_func == None or filter_func(text, start) == False:

                dto = LawDTO(lawname, start=start, face=face)

                law_dto_list.append(dto)

            start = text.find(target, start + 1)

    def _法律の略称ではない商法をブロックする関数(self, text: str, start: int) -> bool:
        """
        「悪徳商法」のような、法律名ではない「〇〇商法」を除外するためのフィルター。

        """

        if start == 0:
            return False

        return 漢字一文字.search(text[start - 1]) != None


漢字一文字 = re.compile(r'\p{Han}')
