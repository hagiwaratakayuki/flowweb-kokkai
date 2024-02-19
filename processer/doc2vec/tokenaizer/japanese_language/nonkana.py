from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re


eisuu = re.compile('^[\w\d]+$', re.A)
kigou = re.compile('^\W+$')
kuuhaku = re.compile('\s+')
kutouten = re.compile('[,。、]')


def extract(results: List[SpecificKeyword], parse_results: List, data):
    nonhiragana_set = set()

    for line, tokens in parse_results:
        line = kutouten.sub(' ',  line)
        for face, data in tokens:
            if eisuu.search(face) is None and kigou.search(face) is None and (data[0] != '名詞' or (data[1] != "一般" and data[2] not in ['地域', '組織'])):
                line = line.replace(face, ' ')

        nonhiragana_set.update(kuuhaku.split(line))
    for nonhiragana in nonhiragana_set:
        if nonhiragana in results:
            continue
        results.append(SpecificKeyword(headword=nonhiragana))

    return results
