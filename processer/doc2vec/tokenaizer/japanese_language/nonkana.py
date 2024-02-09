from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re

pt = re.compile('\p{Hiragana}+')


def extract(results: List[SpecificKeyword], parse_results: List):
    nonhiragana_set = set()

    for line, tokens in parse_results:
        nonhiragana_set.update([t for t in pt.split(line) if t != ''])
    for nonhiragana in nonhiragana_set:
        results.push(SpecificKeyword(headword=nonhiragana))
    return results
