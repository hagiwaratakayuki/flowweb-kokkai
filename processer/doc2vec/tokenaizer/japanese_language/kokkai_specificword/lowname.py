from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword, EqIn
import regex as re

import os
import json
from operator import itemgetter
from collections import defaultdict, deque
from data_loader.dto import DTO
sortkey = itemgetter(1)

section_text = "編章条項節款目"
section_pt = re.compile('(?<!ス.パ.)\d+([' + section_text + '])')
section_rank = {}
section_rank.update({section: i + 1 for i, section in enumerate(section_text)})

アイヌ新法 = "アイヌ新法"

name_index_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/nameindex.json')
ryakusyou_tenchi_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou_tenchi.json')
ryakusyou_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou.json')
with open(file=name_index_path, mode='r', encoding="utf-8") as fp:
    name_index = json.load(fp)
with open(file=ryakusyou_path, mode='r', encoding="utf-8") as fp:
    ryakusyou_dict = json.load(fp)

with open(file=ryakusyou_tenchi_path, mode='r', encoding="utf-8") as fp:
    ryakusyou_tench = json.load(fp)


class EqInShorter:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value


def extract(results: List[SpecificKeyword], parse_results: List, data: DTO):

    target_low = []
    waiting_sections = []
    tail_rank = None
    low_set = set()

    lowword_set = set()
    reverse_dict = {}

    for line, tokens in parse_results:
        canditates_set = set()
        ryakusyou_canditates_set = set()
        line_lows = []
        アイヌ新法が含まれるか = アイヌ新法 in line

        if アイヌ新法が含まれるか is True:
            if data.published >= "2019-01-28":
                アイヌ新法の正式名称 = "アイヌの人々の誇りが尊重される社会を実現するための施策の推進に関する法律"
            else:
                アイヌ新法の正式名称 = "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律"

        for i in range(len(line)-1):
            gram = line[i:i+2]
            canditates = name_index.get(gram)
            ryakusyou_canditates = ryakusyou_tench.get(gram)
            if canditates is not None:
                canditates_set.update(canditates)

            if ryakusyou_canditates is not None:
                ryakusyou_canditates_set.update(ryakusyou_canditates)

        _ryakusyous = [
            canditate for canditate in ryakusyou_canditates_set if canditate in line]

        ryakusyou_index = [EqInShorter(ry) for ry in _ryakusyous]
        not_ryakusyous = [
            canditate for canditate in canditates_set if canditate in line and canditate not in ryakusyou_index]

        not_ryakusyou_index = [EqInShorter(not_ry)
                               for not_ry in not_ryakusyous]
        ryakusyous = [
            canditate for canditate in _ryakusyous if canditate not in not_ryakusyou_index]
        reverse_dict.update(
            {ryakusyou_dict[ryakusyou]: ryakusyou for ryakusyou in ryakusyous if ryakusyou != アイヌ新法})

        lowword_set.update(not_ryakusyous)

        lowword_set.update(ryakusyous)

        line_lows.extend([(canditate, line.find(canditate), 0,)
                          for canditate in not_ryakusyous])

        line_lows.extend([(ryakusyou_dict[ryakusyou],  line.find(
            ryakusyou), 0, ) for ryakusyou in ryakusyous])

        if アイヌ新法が含まれるか is True:
            lowword_set.add(アイヌ新法)
            reverse_dict[アイヌ新法の正式名称] = アイヌ新法
            line_lows.append((アイヌ新法の正式名称,  line.find(アイヌ新法), 0,))
        section_words = [(m.group(0), m.start(), section_rank[m.group(1)], )
                         for m in section_pt.finditer(line)]

        line_lows.extend(section_words)

        lowword_set.update([r[0] for r in section_words])

        line_lows.sort(key=sortkey)

        for face, position, rank in line_lows:

            if tail_rank is None:
                if rank > 0:
                    waiting_sections.append((face, rank,))
                    continue
                tail_rank = 0

                target_low.append((face, 0,))
                waiting_length = len(waiting_sections)
                if waiting_length > 0:
                    waiting_sections.sort(key=sortkey)
                    target_low.extend([r[0] for r in waiting_sections])
                    tail_rank = waiting_sections[waiting_length - 1][1]
                continue

            if rank <= tail_rank:
                low_set.add(tuple(r[0] for r in target_low))
                target_low = [
                    r for r, target_rank in target_low if target_rank < rank]
                target_low.append((face, rank, ))
                tail_rank = rank
                continue
            target_low.append((face, rank, ))

    if len(target_low) > 0:
        low_set.add(tuple(r[0] for r in target_low))

    kws = []

    for low_tupple in low_set:

        headword = low_tupple[0]

        subwords = list(low_tupple[1:])
        index_word = reverse_dict.get(headword)
        is_one_gram = index_word is None

        kw = SpecificKeyword(
            headword=headword, subwords=subwords, is_force=True, is_one_grame=is_one_gram)

        kws.append(kw)

    lowword_list = [EqIn(lowword) for lowword in lowword_set]

    results = [spk for spk in results if spk.headword not in lowword_list]
    results.extend(kws)

    return results
