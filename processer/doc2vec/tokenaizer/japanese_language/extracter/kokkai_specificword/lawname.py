from functools import reduce
from re import X
from typing import Deque, Iterator, List, Tuple
from unittest import result

from numpy import append
from crowler.lib.webapi.twitter import K
from doc2vec.util.specific_keyword import SpecificKeyword, EqIn
import regex as re

import os
import json
from operator import itemgetter
from collections import Counter, defaultdict, deque
from data_loader.dto import DTO

sortkey = itemgetter(1)

section_text = r"編章条項節款目"
section_pt = re.compile(r'(?<!ス.パ.)\d+([' + section_text + r'])')
section_rank = {}
section_rank.update({section: i + 1 for i, section in enumerate(section_text)})

アイヌ新法 = "アイヌ新法"
改正前のアイヌ新法の正式名称 = "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律"

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


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


def extract(results: List[SpecificKeyword], parse_results: List, data: DTO):

    target_law = []
    waiting_sections = []
    waiting_line_numbers = set()

    tail_rank = None
    law_index = defaultdict(set)

    lawword_set = set()
    reverse_dict = defaultdict(set)
    line_number = -1
    all_text = ''.join([parse_result[0] for parse_result in parse_results])
    law_count = all_text.count('法')
    if law_count == 0:
        return results
    standard_phrase_count = 0
    detected_phrases = set()
    for phrase in law_standard_phrases:
        detected_phrase_count = all_text.count(phrase)

        standard_phrase_count += detected_phrase_count
        if detected_phrase_count > 0:
            detected_phrases.add(phrase)
    for detected_phrase in detected_phrases:

        results.append(SpecificKeyword(
            headword=detected_phrase, is_force=True))

    if law_count == standard_phrase_count:
        return results

    for line, tokens in parse_results:

        line_number += 1

        canditates_counter = Counter()
        ryakusyou_canditates_counter = Counter()
        line_laws = []
        アイヌ新法が含まれるか = アイヌ新法 in line

        if アイヌ新法が含まれるか is True:
            if data.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = 改正前のアイヌ新法の正式名称
            lawword_set.add(アイヌ新法)
            reverse_dict[アイヌ新法の正式名称].add(アイヌ新法)
            line_laws.append((アイヌ新法の正式名称, line.find(アイヌ新法), 0,))

        活火山法の検索結果 = 活火山法の略称候補.search(line)
        活火山法が含まれるか = 活火山法の検索結果 is not None
        if 活火山法が含まれるか is True:
            活火山法の略称 = 活火山法の検索結果.group(0)
            if data.published >= "1973-7-13":
                活火山法の正式名称 = 改正後の活火山法の正式名称
            else:
                活火山法の正式名称 = 改正前の活火山法の正式名称
            lawword_set.add(活火山法の略称)
            reverse_dict[活火山法の正式名称].add(活火山法の略称)
            line_laws.append((活火山法の正式名称, line.find(活火山法の略称), 0,))

        for i in range(len(line) - 1):
            gram = line[i:i + 2]
            canditates_counter.update(name_index.get(gram, []))

            ryakusyou_canditates_counter.update(ryakusyou_tench.get(gram, []))

        _ryakusyous = [
            canditate for canditate in ryakusyou_canditates_counter if canditate in line]

        ryakusyou_index = [EqInShorter(ry) for ry in _ryakusyous]
        not_ryakusyous = [
            canditate for canditate in canditates_counter if canditate in line and canditate not in ryakusyou_index]

        not_ryakusyou_index = [EqInShorter(not_ry)
                               for not_ry in not_ryakusyous]
        ryakusyous = [
            canditate for canditate in _ryakusyous if canditate not in not_ryakusyou_index]
        for ryakusyou in ryakusyous:
            if ryakusyou == アイヌ新法:
                continue

            reverse_dict[ryakusyou_dict[ryakusyou]].add(ryakusyou)

        lawword_set.update(not_ryakusyous)

        lawword_set.update(ryakusyous)

        line_laws.extend([(canditate, line.find(canditate), 0,)
                          for canditate in not_ryakusyous])

        line_laws.extend([(ryakusyou_dict[ryakusyou], line.find(
            ryakusyou), 0, ) for ryakusyou in ryakusyous])

        section_words = [(m.group(0), m.start(), section_rank[m.group(1)], )
                         for m in section_pt.finditer(line)]

        line_laws.extend(section_words)

        lawword_set.update([r[0] for r in section_words])

        line_laws.sort(key=sortkey)

        for face, position, rank in line_laws:

            if tail_rank is None:
                waiting_line_numbers.add(line_number)
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
                    law_index[k].add(line_number)
                    law_index[k].update(waiting_line_numbers)
                target_law = [
                    (r, target_rank, ) for r, target_rank in target_law if target_rank < rank]
                target_law.append((face, rank, ))

                tail_rank = rank

                if rank == 0:
                    waiting_sections = []
                    waiting_line_numbers = set()
                continue
            target_law.append((face, rank, ))

        if (tail_rank != None) and (len(target_law) != 0):

            k = tuple(r[0] for r in target_law)
            law_index[k].add(line_number)
            law_index[k].update(waiting_line_numbers)

    kws = []

    empty_set = set()

    for law_tupple, line_numbers in law_index.items():

        headword = law_tupple[0]

        subwords = list(law_tupple[1:])

        target_words = reverse_dict.get(headword, [])

        kw = SpecificKeyword(
            headword=headword, subwords=subwords, is_force=True, line_numbers=line_numbers, target_words=target_words, is_allaw_add_multiple_subword=True)
        kws.append(kw)

    # pending
    # lawword_list = [EqIn(lawword) for lawword in lawword_set]

    # results = [spk for spk in results if spk.headword not in lawword_list]
    results.extend(kws)

    return results
