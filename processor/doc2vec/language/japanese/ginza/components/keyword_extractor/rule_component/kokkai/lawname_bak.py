

from multiprocessing import context
from typing import Deque, Iterator, List, Optional, Set, Tuple, Option


import numpy as np


from crowler.lib.webapi.twitter import K
from doc2vec.util.specified_keyword import SpecifiedKeyword, EqIn
import regex as re

from spacy.tokens import Token, Doc, Span
import os
import json
from operator import itemgetter
from collections import Counter, defaultdict, deque
from data_loader.kokkai import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.keyword_extractor.protocol import ExtractResultDTO, KeywordExtractRule
from doc2vec.spacy.japanese_language.components.keyword_extract.rule.kokkai.discussion_context import DiscussionContext
from doc2vec.tokenaizer.japanese_language.extracter.kokkai_specificword import lawname


positionkey = itemgetter(1)

章としての区分を表す単語 = "編章条項節款目"
区分の最大深さ = len(章としての区分を表す単語) - 1
section_pt = re.compile(r'\d+.')
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

連続章区分表現の接続語 = {'の', '第'}
記号を表すパターン = re.compile(r'^\W+$')


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


class RelativeRank:
    fluctuation: int

    def __init__(self, fluctuation=0):
        self.fluctuation = fluctuation


class RankedPath:
    def __init__(self):
        self.clear()

    def _reverse_search(self, needle_rank):
        reverse_index = -1
        limit = self.len * -1
        while limit <= reverse_index:
            rank = self.path[reverse_index][1]
            if (rank is not None and needle_rank is not None and rank < needle_rank) or (needle_rank is None and rank != None):

                return reverse_index + 1, limit
            if needle_rank == rank:
                break
            reverse_index = -1
        return reverse_index, limit

    def clear(self):
        self.path = []
        self.len = 0


class WaitingSections(RankedPath):
    def clear(self):
        super().clear()
        self.paths = [self.path]
        self.is_none_rank_exist = False

    def add(self, face, rank):
        if self.len == 0:
            self.path.append((face, rank,))
        reverse_index, limit = self._reverse_search(needle_rank=rank)
        if reverse_index == 0:
            self.path.append((face, rank,))
        elif reverse_index < limit:
            for path in self.paths:
                path.insert(0, (face, rank,))
        else:
            next_path = self.path[:reverse_index]
            next_path.append((face, rank,))
            self.path = next_path
            self.paths.append(next_path)


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO):
        doc_len = len(doc)
        doc_limit = doc_len - 1
        target_law = []

        waiting_sections = WaitingSections()

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
        law_list = []
        アイヌ新法が含まれるか = アイヌ新法 in doc.text

        if アイヌ新法が含まれるか is True:
            if dto.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称

            law_list.append((アイヌ新法の正式名称, doc.text.find(アイヌ新法),))
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

            law_list.append((活火山法の正式名称, doc.text.find(活火山法の略称), 0,))

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
            law_2_overwrite[活火山法] = False

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

        for lawname in 発見された正式名称のリスト:
            positions = self._get_positions(doc, lawname)

            for position in positions:
                law_list.append((lawname, position, lawname, ))
        for 法律名の略称 in 法律名の略称のリスト:
            positions = self._get_positions(doc, 法律名の略称)
            法律の正式名称 = 略称と正式名称の対応表[法律名の略称]

            for position in self._get_positions(doc, 法律名の略称):
                law_list.append((法律の正式名称, position, 法律名の略称,))

        # line_laws.extend((m.group(0), m.start(), section_rank[m.group(1)], )
        #             )

        position = 0

        #  条項目抽出と一体化する
        # 　法律名の結合処理とも一体化する
        # 『の』でつながっている限りrankは上がる
        # 　『の』以外があったら並列
        #       その後で条項目法律名がなく『の』が出たらrankリセット
        law_list.sort(key=positionkey)
        target_law_index = 0
        law_list_len = len(law_list)

        is_wait = False
        lawname = None
        if law_list_len == 0:
            is_context_exist, lawname = self.context.get_data(dto=dto)
            if not is_context_exist:
                return results

            next_law_position = doc_len
        else:
            lawname = law_list[0][0]
            next_law_position = law_list[1][1]
        if not is_wait:
            self.context.set_data(data=lawname, dto=dto)

        区分の深度 = 0
        waiting_path = []
        waiting_path_list = [waiting_path]

        index = 0
        数値の後である = False
        # 段階表現　3条の1の2、みたいな表現のこと
        段階表現の最初の部分である = True
        段階表現で変化した区分の深さ = 0

        law_expressions = set()
        章としての区分を表す単語の後か = False
        未決定の区分が存在するか = False
        未決定の区分のリスト: List[List] = []
        数値のみの表記の後か = False
        while index < doc_len:
            token = doc[index]
            token_len = len(token)
            index += 1
            if next_law_position <= position or position + token_len > next_law_position:
                章としての区分を表す単語の後か = False
                未決定の区分が存在するか = False
                数値のみの表記の後か = False
                段階表現で変化した区分の深さ = 0
                段階表現の最初の部分である = True
                未決定の区分のリスト = []
                target_tokens.append(token)

                limit_position = len(lawname) + next_law_position

                position += token_len
                self._add_law_expressions(
                    lawname=lawname, waiting_path_list=waiting_path_list, lawexpessions=law_expressions)
                waiting_path = []
                waiting_path_list = [waiting_path]
                while index < doc_len and position < limit_position:
                    token = doc[index]
                    target_tokens.append(token)
                    position += len(token)
                    index += 1
                target_law_index += 1
                diff = law_list_len - target_law_index
                if diff <= 0:
                    next_law_position = doc_len
                if diff == 1:
                    lawname = law_list[target_law_index][0]
                    next_law_position = doc_len
                else:
                    lawname = law_list[target_law_index][0]
                    next_law_position = law_list[target_law_index + 1][1]
                continue

            position += token_len
            if token.dep_ == 'NUM':
                candiate_token = token
                数値の後である = True
                continue
            if 数値の後である:
                if token.norm_ == 'の':
                    数値のみの表記の後か = False
                    if 章としての区分を表す単語の後か:
                        if 段階表現の最初の部分である and 段階表現で変化した区分の深さ > 0:
                            カットすべき区分の深度 = 区分の深度 - 段階表現で変化した区分の深さ
                            next_waiting_path = [
                                r for r in waiting_path if r[1] < カットすべき区分の深度]
                            waiting_path_list.append(next_waiting_path)
                            waiting_path = next_waiting_path

                        waiting_path.append(
                            (candiate_token.norm_ + 章としての区分を表す単語[区分の深度], 区分の深度))
                    else:
                        未決定の区分が存在するか = True
                        if 段階表現の最初の部分である and 段階表現で変化した区分の深さ > 0:

                            waiting_path = []
                            waiting_path_list.append(waiting_path)
                            未決定の区分のリスト.append(waiting_path)

                        waiting_path.append((candiate_token.norm_, -1))
                    if 段階表現の最初の部分である:
                        段階表現の最初の部分である = False
                        区分の深度 -= 段階表現で変化した区分の深さ
                        段階表現で変化した区分の深さ = 2
                    else:
                        段階表現で変化した区分の深さ += 1
                    区分の深度 += 1
                    区分の深度 = min(max(区分の深度, 2),
                                区分の最大深さ)

                elif token.norm_ in 章の区分と数値の変換表:
                    章としての区分を表す単語の後か = True
                    数値のみの表記の後か = False

                    段階表現で変化した区分の深さ = 0
                    段階表現の最初の部分である = True
                    対象の区分 = 章の区分と数値の変換表[token.norm_]
                    if 未決定の区分が存在するか:
                        index_ = index

                        挿入する区分の候補のリスト = [
                            (candiate_token.norm_ + token.norm_, 対象の区分,)]
                        倒置表現において章表現が連続しているか = False
                        倒置表現の項目番号 = -1

                        position
                        while index_ <=:
                            target_token_ = doc[index_]
                            index_ += 1
                            if target_token_.dep_ == 'NUM':
                                倒置表現において章表現が連続しているか = True
                                倒置表現の項目番号 =

                            if target_token_.norm_ in 連続章区分表現の接続語:
                                continue

                            if 記号を表すパターン.search(target_token_.norm_):
                                break

                        for 未決定の区分 in 未決定の区分のリスト:
                            index = 0
                            for 未決定の要素 in 未決定の区分:
                                推定された区分の深さ = min(index + 1 + 対象の区分, 区分の最大深さ)
                                推定された区分表現 = 章としての区分を表す単語[推定された区分の深さ]
                                未決定の区分[index] = (推定された区分表現, 推定された区分の深さ,)
                            if 対象の区分 > 1:
                                未決定の区分.insert(0, 挿入する区分)

                    else:
                        if 区分の深度 >= 対象の区分:

                            next_path = [
                                (区分表現, この要素での区分の深さ,) for 区分表現, この要素での区分の深さ in waiting_sections if この要素での区分の深さ < 対象の区分]
                            next_path.append(
                                (candiate_token.norm_ + token.norm_, 対象の区分,))
                            waiting_path_list.append(next_path)
                            waiting_path = next_path
                        区分の深度 = 対象の区分 + 1
                        if 対象の区分 <= 1:  # 章と編は無視
                            continue
                        waiting_path.append(
                            (candiate_token.norm_ + token.norm_, 対象の区分,))
                elif 漢字でないパターン.search(token.norm_):
                    # 並列のパターンならば分岐
                    # 　章としての区分の後ならば推定
                    if 数値のみの表記の後か:
                        next_path = waiting_path[:-1]
                        if 章としての区分を表す単語の後か:
                            next_path.append()
                        else:
                            pass

        for law_tupple, line_numbers in law_index.items():
            if law_tupple[0] == "商法" and 商売の方法または金商法の略称の一部としての商法である is True:
                continue
            headword = law_tupple[0]

            subwords = list(law_tupple[1:])

            # todo 効率よく
            target_words = reverse_dict.get(headword, [])
            tokens = set()
            for word in target_words + law_tupple:
                tokens.update(self._get_hittokens(doc=doc, word=word))

            kw = SpecifiedKeyword(
                headword=headword, subwords=subwords, is_force=True, tokens=tokens, target_words=target_words, is_allow_add_multiple_subword=True)
            results.add_keyword(
                keyword=kw, is_overwrite_token=law_2_overwrite.get(headword, True))
        for headword in additional_law_words:
            kw = SpecifiedKeyword(
                headword=headword, is_force=True, tokens=target_tokens.get(headword, set()))
            results.add_keyword(
                kw, is_overwrite_token=law_2_overwrite.get(headword, True))

        return results

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

    def _get_positions(self, doc: Doc, needle):
        splited = doc.text.split(needle)
        position = 0
        needle_len = len(needle)
        positions = deque()
        for row in splited:
            position += len(row)
            positions.append(position)
            position += needle_len
        return positions

    def _add_law_expressions(self, lawname, waiting_path_list, lawexpessions: Set):

        for waiting_path in waiting_path_list:
            is_path_exist = True
            lawexpession = (lawname, ) + tuple(r[1] for r in waiting_path)
            lawexpessions.add(lawexpession)
