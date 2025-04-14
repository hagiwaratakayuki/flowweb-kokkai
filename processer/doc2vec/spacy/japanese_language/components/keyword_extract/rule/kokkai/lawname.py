

from typing import Deque, Iterator, List, Tuple
from unittest import result

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


sortkey = itemgetter(1)

section_text = r"編章条項節款目"
section_pt = re.compile(r'(?<!ス.パ.)\d+([' + section_text + r'])(?!委員会)')
section_rank = {}
section_rank.update({section: i + 1 for i, section in enumerate(section_text)})

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
    ryakusyou_dict = json.load(fp)

with open(file=ryakusyou_tenchi_path, mode='r', encoding="utf-8") as fp:
    ryakusyou_tench = json.load(fp)
law_standard_phrases = ['法の下の平等', '法の支配']
商売の方法または金商法の略称の一部としての商法を表すパターン = re.compile(r'\p{Han}+商法')


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


class Rule(KeywordExtractRule):
    context: DiscussionContext

    def __init__(self):
        self.context = DiscussionContext()

    def execute(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO):

        target_law = []
        waiting_sections = []
        waiting_line_numbers = set()

        tail_rank = None
        law_index = defaultdict(set)

        lawword_set = set()
        reverse_dict = defaultdict(set)
        sent_number = -1
        all_text = doc.text
        law_count = all_text.count('法')
        if law_count == 0:
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
        # TODO　トークンの探索処理を追加する
        # TODO　探査処理の結果を保存できるようにする
        law_2_tokens = defaultdict(set)
        law_2_overwrite = {}
        for sent in doc.sents:

            sent_number += 1

            canditates_set = set()
            ryakusyou_canditates_set = set()
            line_laws = []
            アイヌ新法が含まれるか = アイヌ新法 in sent

            if アイヌ新法が含まれるか is True:
                if dto.published >= "2019-01-28":
                    アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
                else:
                    アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称
                lawword_set.add(アイヌ新法)
                reverse_dict[アイヌ新法の正式名称].add(アイヌ新法)
                line_laws.append((アイヌ新法の正式名称, sent.find(アイヌ新法), 0,))
                law_2_tokens[アイヌ新法の正式名称].update(
                    self._get_hittokens(sent=sent, word=アイヌ新法))

            活火山法の検索結果 = 活火山法の略称候補.search(sent)
            活火山法が含まれるか = 活火山法の検索結果 is not None
            if 活火山法が含まれるか is True:
                additional_law_words.add(活火山法)
                活火山法の略称 = 活火山法の検索結果.group(0)
                if dto.published >= "1973-7-13":
                    活火山法の正式名称 = 改正後の活火山法の正式名称
                else:
                    活火山法の正式名称 = 改正前の活火山法の正式名称
                lawword_set.add(活火山法の略称)
                reverse_dict[活火山法の正式名称].add(活火山法の略称)
                line_laws.append((活火山法の正式名称, sent.find(活火山法の略称), 0,))
                law_2_tokens[活火山法の正式名称].update(
                    self._get_hittokens(sent=sent, word=活火山法の略称))
            改正前の活火山法の正式名称が存在する = 改正前の活火山法の正式名称 in sent
            改正後の活火山法の正式名称が存在する = 改正後の活火山法の正式名称 in sent
            if 改正前の活火山法の正式名称が存在する or 改正後の活火山法の正式名称が存在する:
                additional_law_words.add(活火山法)
                if 改正前の活火山法の正式名称が存在する:
                    law_2_tokens[活火山法].update(
                        self._get_hittokens(sent, word=改正前の活火山法の正式名称))
                if 改正後の活火山法の正式名称が存在する:
                    law_2_tokens[活火山法].update(
                        self._get_hittokens(sent=sent, word=改正後の活火山法の正式名称))
                law_2_overwrite[活火山法] = False

            for i in range(len(sent) - 1):
                gram = sent[i:i + 2]
                canditates_set.update(name_index.get(gram, []))

                ryakusyou_canditates_set.update(
                    ryakusyou_tench.get(gram, []))

            _ryakusyous = [
                canditate for canditate in ryakusyou_canditates_set if canditate in sent]

            ryakusyou_index = [EqInShorter(ry) for ry in _ryakusyous]
            not_ryakusyous = [
                canditate for canditate in canditates_set if canditate in sent and canditate not in ryakusyou_index]

            not_ryakusyou_index = [EqInShorter(not_ry)
                                   for not_ry in not_ryakusyous]

            ryakusyous = [
                canditate for canditate in _ryakusyous if canditate not in not_ryakusyou_index]
            for ryakusyou in ryakusyous:
                if ryakusyou == アイヌ新法 or ryakusyou == 活火山法:
                    continue

                reverse_dict[ryakusyou_dict[ryakusyou]].add(ryakusyou)
            if "商法" in not_ryakusyous:

                商売の方法または金商法の略称の一部としての商法である |= 商売の方法または金商法の略称の一部としての商法を表すパターン.search(
                    sent) is not None

            lawword_set.update(not_ryakusyous)

            lawword_set.update(ryakusyous)

            line_laws.extend([(canditate, sent.find(canditate), 0,)
                              for canditate in not_ryakusyous])

            line_laws.extend([(ryakusyou_dict[ryakusyou], sent.find(
                ryakusyou), 0, ) for ryakusyou in ryakusyous])

            section_words = [(m.group(0), m.start(), section_rank[m.group(1)], )
                             for m in section_pt.finditer(sent)]

            line_laws.extend(section_words)

            lawword_set.update([r[0] for r in section_words])

            line_laws.sort(key=sortkey)

            for face, position, rank in line_laws:
                tokens = self._get_hittokens(sent=sent, word=face)
                if tail_rank is None:
                    waiting_line_numbers.add(sent_number)
                    if rank > 0:

                        waiting_sections.append((face, rank,))
                        continue

                    tail_rank = 0

                    target_law.append((face, 0,))
                    waiting_length = len(waiting_sections)
                    if waiting_length > 0:
                        waiting_sections.sort(key=sortkey)
                        target_law.extend(waiting_sections)
                        tail_rank = waiting_sections[waiting_length - 1][1]
                    continue

                if rank <= tail_rank:

                    if (tail_rank != None) and (len(target_law) != 0):
                        k = tuple(r[0] for r in target_law)
                        law_index[k].add(sent_number)
                        law_index[k].update(waiting_line_numbers)
                    target_law = [
                        (r, target_rank, ) for r, target_rank in target_law if target_rank < rank]
                    target_law.append((face, rank, ))

                    tail_rank = rank

                    if rank == 0:
                        waiting_sections = []
                        waiting_line_numbers = set()
                    continue
                tail_rank = rank
                target_law.append((face, rank, ))

            if (tail_rank != None) and (len(target_law) != 0):

                k = tuple(r[0] for r in target_law)
                law_index[k].add(sent_number)
                law_index[k].update(waiting_line_numbers)

        kws = []

        for law_tupple, line_numbers in law_index.items():
            if law_tupple[0] == "商法" and 商売の方法または金商法の略称の一部としての商法である is True:
                continue
            headword = law_tupple[0]

            subwords = list(law_tupple[1:])

            target_words = reverse_dict.get(headword, [])
            tokens = set()
            for word in target_words + law_tupple:
                tokens.update(self._get_hittokens(sent=sent, word=word))

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

    def _get_hittokens(self, sent: Span, word: str):
        tokens = []
        is_matched = False
        for token in sent:

            if token.lemma_ not in word and word not in token.lemma_:
                if is_matched:
                    break
                continue
            is_matched = True
            tokens.append(token)

        return tokens
