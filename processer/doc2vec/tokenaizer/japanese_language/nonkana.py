from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re


eisuu = re.compile('^[\w\d]+$', re.A)
kigou = re.compile('^\W+$')
kuuhaku = re.compile('\s+')


def extract(results: List[SpecificKeyword], parse_results: List):
    nonhiragana_set = set()

    for line, tokens in parse_results:

        for face, data in tokens:
            if eisuu.search(face) is None and kigou.search(face) is None and (data[0] != '名詞' or (data[1] != "一般" and data[2] not in ['地域', '組織'])):
                line = line.replace(face, ' ')

        nonhiragana_set.update([t for t in kuuhaku.split(line) if len(t) > 1])
    for nonhiragana in nonhiragana_set:
        results.append(SpecificKeyword(headword=nonhiragana))
    return results
