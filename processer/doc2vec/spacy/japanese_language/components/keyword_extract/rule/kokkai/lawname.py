

from multiprocessing import context
from typing import Deque, Iterator, List, Optional, Tuple, Option


import numpy as np


from doc2vec.util.specified_keyword import SpecifiedKeyword, EqIn
import regex as re

from spacy.tokens import Token, Doc, Span
import os
import json
from operator import itemgetter
from collections import Counter, defaultdict, deque
from data_loader.kokkai import DTO
from doc2vec.protocol.sentiment import SentimentResult
from doc2vec.spacy.components.keyword_extracter.protocol import ExtractResultDTO, KeywordExtractRule
from doc2vec.spacy.japanese_language.components.keyword_extract.rule.kokkai.discussion_context import DiscussionContext
from processer.doc2vec.tokenaizer.japanese_language.extracter.kokkai_specificword import lawname


positionkey = itemgetter(1)

section_text = "編章条項節款目"
max_section_depth = len(section_text) - 1
section_pt = re.compile(r'\d+.')
section_to_depth = {section_text[i]: i for i in range(len(section_text))}
スーパー301条対策のパターン = re.compile('ス.パ.')
委員会 = "委員会"
数字と項目名のパターン = r'\d[' + section_text + ']'

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
        waiting_sent_numbers = set()

        tail_rank = None
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

        law_2_tokens = defaultdict(set)
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

            # reverse_dict[アイヌ新法の正式名称].add(アイヌ新法)
            law_list.append((アイヌ新法の正式名称, doc.text.find(アイヌ新法), 0,))
            law_2_tokens[アイヌ新法の正式名称].update(
                self._get_hittokens(doc=doc, word=アイヌ新法))

        活火山法の検索結果 = 活火山法の略称候補.search(doc.text)
        活火山法が含まれるか = 活火山法の検索結果 is not None
        if 活火山法が含まれるか is True:
            additional_law_words.add(活火山法)
            活火山法の略称 = 活火山法の検索結果.group(0)
            if dto.published >= "1973-7-13":
                活火山法の正式名称 = 改正後の活火山法の正式名称
            else:
                活火山法の正式名称 = 改正前の活火山法の正式名称

            # reverse_dict[活火山法の正式名称].add(活火山法の略称)
            law_list.append((活火山法の正式名称, doc.text.find(活火山法の略称), 0,))
            law_2_tokens[活火山法の正式名称].update(
                self._get_hittokens(doc=doc, word=活火山法の略称))
        改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in doc.text
        改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in doc.text
        if 改正前の活火山法の正式名称が存在する or 改正後の活火山法の正式名称が存在する:
            additional_law_words.add(活火山法)
            if 改正前の活火山法の正式名称が存在する:
                law_2_tokens[活火山法].update(
                    self._get_hittokens(doc, word=改正前の活火山法の正式名称))
            if 改正後の活火山法の正式名称が存在する:
                law_2_tokens[活火山法].update(
                    self._get_hittokens(doc=doc, word=改正後の活火山法の正式名称))
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
        sections = []
        for m in section_pt.finditer(doc.text):

            # line_laws.extend((m.group(0), m.start(), section_rank[m.group(1)], )
            #                 )

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
        # 待機状態ならば、waiting_sectionに
        # そうでないならば　項目名を足す
        checked_tokens = set()
        depth = 0
        waiting_path = []
        target_tokens = {}
        waiting_tokens = set()
        waiting_tokens_list = [waiting_tokens]
        index = 0
        前回のので繋がる数値表現の深さ = 0
        while index < doc_len:
            token = doc[index]
            token_len = len(token)
            if next_law_position <= position or position + token_len > next_law_position:
                前回のので繋がる数値表現の深さ = 0
                law_tokens = set()
                law_tokens.add(tokens)
                index += 1
                limit_position = len(lawname) + next_law_position

                position += token_len
                while index < doc_len and position < limit_position:
                    token = doc[index]
                    law_2_tokens.add(token)
                    position += len(token)
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
        # ここから下廃止
        for face, position, rank in law_list:
            # tokens = self._get_hittokens(sent=sent, word=face) ここは略称処理に持っていく
            if tail_rank is None:

                waiting_sent_numbers.add(sent_number)
                if rank == None or rank > 0:

                    waiting_sections.add((face, rank,))
                    continue

                tail_rank = 0

                target_law.append((face, 0,))
                last_index = len(waiting_sections.paths)
                index = 0
                while index < last_index:
                    waiting_path = waiting_sections.paths[index]
                    index += 1
                    if index == last_index:
                        target_law.extend(waiting_path)
                        tail_rank = waiting_sections[-1][1]
                    else:
                        k = tuple(r[0] for r in waiting_path)
                        law_index[k].add(sent_number)
                        law_index[k].update(waiting_sent_numbers)
                waiting_sections.clear()
                continue

            if rank <= tail_rank:

                if (tail_rank != None) and (len(target_law) != 0):
                    k = tuple(r[0] for r in target_law)
                    law_index[k].add(sent_number)
                    law_index[k].update(waiting_sent_numbers)
                target_law = [
                    (r, target_rank, ) for r, target_rank in target_law if target_rank < rank]
                target_law.append((face, rank, ))

                tail_rank = rank

                if rank == 0:
                    waiting_sections.clear()
                    waiting_sent_numbers = set()
                continue
            tail_rank = rank
            target_law.append((face, rank, ))

        if (tail_rank != None) and (len(target_law) != 0):

            k = tuple(r[0] for r in target_law)
            law_index[k].add(sent_number)
            law_index[k].update(waiting_sent_numbers)

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
                headword=headword, subwords=subwords, is_force=True, source_ids=tokens, target_words=target_words, is_allow_add_multiple_subword=True)
            results.add_keyword(
                keyword=kw, is_overwrite_token=law_2_overwrite.get(headword, True))
        for headword in additional_law_words:
            kw = SpecifiedKeyword(
                headword=headword, is_force=True, source_ids=law_2_tokens.get(headword, set()))
            results.add_keyword(
                kw, is_overwrite_token=law_2_overwrite.get(headword, True))

        return results

    def _get_hittokens(self, doc: Doc, word: str):
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
