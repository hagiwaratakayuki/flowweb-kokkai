from functools import reduce
from re import X
from typing import Deque, Iterator, List, Tuple
from unittest import result

from numpy import append
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
low_standard_phrases = ['法の下の平等', '法の支配']


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


def extract(results: List[SpecificKeyword], parse_results: List, data: DTO):

    target_low = []
    waiting_sections = []
    waiting_line_numbers = set()

    tail_rank = None
    low_index = defaultdict(set)

    lowword_set = set()
    reverse_dict = defaultdict(set)
    line_number = -1
    all_text = ''.join([parse_result[0] for parse_result in parse_results])
    low_count = all_text.count('法')
    if low_count == 0:
        return results
    standard_phrase_count = 0
    detected_phrases = set()
    for phrase in low_standard_phrases:
        detected_phrase_count = all_text.count(phrase)

        standard_phrase_count += detected_phrase_count
        if detected_phrase_count > 0:
            detected_phrases.add(phrase)
    for detected_phrase in detected_phrases:

        results.append(SpecificKeyword(
            headword=detected_phrase, is_force=True))

    if low_count == standard_phrase_count:
        return results

    for line, tokens in parse_results:

        line_number += 1

        canditates_counter = Counter()
        ryakusyou_canditates_counter = Counter()
        line_lows = []
        アイヌ新法が含まれるか = アイヌ新法 in line

        if アイヌ新法が含まれるか is True:
            if data.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律"
            lowword_set.add(アイヌ新法)
            reverse_dict[アイヌ新法の正式名称].add(アイヌ新法)
            line_lows.append((アイヌ新法の正式名称, line.find(アイヌ新法), 0,))
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

        lowword_set.update(not_ryakusyous)

        lowword_set.update(ryakusyous)

        line_lows.extend([(canditate, line.find(canditate), 0,)
                          for canditate in not_ryakusyous])

        line_lows.extend([(ryakusyou_dict[ryakusyou], line.find(
            ryakusyou), 0, ) for ryakusyou in ryakusyous])

        section_words = [(m.group(0), m.start(), section_rank[m.group(1)], )
                         for m in section_pt.finditer(line)]

        line_lows.extend(section_words)

        lowword_set.update([r[0] for r in section_words])

        line_lows.sort(key=sortkey)

        for face, position, rank in line_lows:

            if tail_rank is None:
                waiting_line_numbers.add(line_number)
                if rank > 0:

                    waiting_sections.append((face, rank,))
                    continue

                tail_rank = 0

                target_low.append((face, 0,))
                waiting_length = len(waiting_sections)
                if waiting_length > 0:
                    waiting_sections.sort(key=sortkey)
                    target_low.extend(waiting_sections)
                    tail_rank = waiting_sections[waiting_length - 1][1]
                continue

            if rank <= tail_rank:

                if (tail_rank != None) and (len(target_low) != 0):
                    k = tuple(r[0] for r in target_low)
                    low_index[k].add(line_number)
                    low_index[k].update(waiting_line_numbers)
                target_low = [
                    (r, target_rank, ) for r, target_rank in target_low if target_rank < rank]
                target_low.append((face, rank, ))

                tail_rank = rank

                if rank == 0:
                    waiting_sections = []
                    waiting_line_numbers = set()
                continue
            target_low.append((face, rank, ))

        if (tail_rank != None) and (len(target_low) != 0):

            k = tuple(r[0] for r in target_low)
            low_index[k].add(line_number)
            low_index[k].update(waiting_line_numbers)

    kws = []

    empty_set = set()

    for low_tupple, line_numbers in low_index.items():

        headword = low_tupple[0]

        subwords = list(low_tupple[1:])

        target_words = reverse_dict.get(headword, [])

        kw = SpecificKeyword(
            headword=headword, subwords=subwords, is_force=True, line_numbers=line_numbers, target_words=target_words, is_allow_add_multiple_subword=True)
        kws.append(kw)

    # pending
    # lowword_list = [EqIn(lowword) for lowword in lowword_set]

    # results = [spk for spk in results if spk.headword not in lowword_list]
    results.extend(kws)

    return results
