from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re
blockpattern = re.compile(
    '^[\W\p{Katakana}]+$|^お|^[^\p{Han}]*\p{Han}[^\p{Han}]*$')


def extract(results: List[SpecificKeyword], parse_results):
    combine_set = set()

    for line, tokens in parse_results:
        meishies = []
        sahens = []

        for face, data in tokens:
            if data[0] != '名詞':
                continue
            if data[1] == 'サ変' and blockpattern.search(face) is None:
                sahens.append(face)

            if data[1] == '一般':
                meishies.append(face)
        for meishi in meishies:
            for sahen in sahens:
                combine_set.update((meishi, sahen,))

    new_results = []
    for headword, subword in combine_set:
        try:
            exist_index = results.index(headword)
            exist_word = results[exist_index]
            if len(headword) > len(exist_word.headword):
                exist_word.headword = headword
            if subword not in exist_word.subwords:
                exist_word.add_subword(subword)

        except ValueError:
            new_results.append(SpecificKeyword(
                headword=headword, subwords=[subword]))
    results.extend(new_results)
    return results
