from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re
import os
import json
from collections import defaultdict

name_index_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/nameindex.json')
ryakusyou_tenchi_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou_tenchi.json')
ryakusyou_path = os.path.realpath(
    'doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou.json')
with open(file=name_index_path, mode='r', encoding="utf-8") as fp:
    name_index = json.load(fp)
with open(file=ryakusyou_path, mode='r', encoding="utf-8") as fp:
    ryakusyou = json.load(fp)

with open(file=ryakusyou_tenchi_path, mode='r', encoding="utf-8") as fp:
    ryakusyou_tench = json.load(fp)

section_pt = re.compile('\d+条')
empty_set = set()


def extract(results: List[SpecificKeyword], parse_results: List):

    target_lows = defaultdict(set)
    prev_lows = {}

    for line, tokens in parse_results:
        canditates_set = set()
        ryakusyou_canditates_set = set()
        line_lows = set()
        for i in range(len(line)-1):
            gram = line[i:i+2]
            canditates = name_index.get(gram)
            if canditates is not None:
                canditates_set.update(canditates)
            ryakusyou_canditates = ryakusyou_tench.get(gram)
            if ryakusyou_canditates is not None:
                ryakusyou_canditates_set.update(ryakusyou_canditates)
            line_lows.update([(canditate, line.find(canditate), )
                             for canditate in canditates if canditate in line])
            line_lows.update([(ryakusyou[canditate],  line.find(canditate),)
                             for canditate in ryakusyou_canditates if canditate in line])

        is_empty = line_lows == empty_set
        if not is_empty:
            _prev_lows = {}
            for line_low in line_lows:
                low_name = line_low[0]
                target_low = target_lows[low_name]
                _prev_lows[line_low] = target_low
            prev_lows = _prev_lows

        number_position = -1
        for section_number in section_pt.findall(line):

            if is_empty == False:
                number_position = line.find(section_number)

            for line_low, section_number_set in prev_lows.items():
                low_name, position = line_low
                if is_empty == True or number_position > position:
                    section_number_set.add(section_number)
    for low_name, section_number_set in target_lows:
        results = [result for result in results if results != low_name]
        if section_number_set == empty_set:
            results.append(SpecificKeyword(headword=low_name, is_force=True))
            continue
        for section_number in section_number_set:
            results.append(SpecificKeyword(headword=low_name,
                           subwords=[section_number], is_force=True))
    return results
