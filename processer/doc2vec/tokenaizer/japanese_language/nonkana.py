from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re


eisuu = re.compile('^[\w\d]+$', re.A)
kigou = re.compile('^\W+$')
kuuhaku = re.compile('\s+')
nonhiragana_pt = re.compile('[\p{Hiragana},。、]')


def extract(results: List[SpecificKeyword], parse_results: List, data):
    nonhiragana_set = set()

    for line, tokens in parse_results:
        blockset = set()
        for face, data in tokens:

            if eisuu.search(face) is None and kigou.search(face) is None and (data[0] != '名詞' or (data[1] != "普通" and data[2] not in ['地域', '組織'])):
                blockset.add(face)

        nonhiragana_set.update(
            [splited for splited in nonhiragana_pt.split(line) if splited not in blockset and len(splited) > 1])

    for nonhiragana in nonhiragana_set:
        if nonhiragana in results:
            continue
        results.append(SpecificKeyword(
            headword=nonhiragana, is_one_grame=True))

    return results
