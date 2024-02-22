from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re
meishi_blockpattern = re.compile('[所々]$')
sahen_blockpattern = re.compile(
    '^[\W\p{Katakana}]+$|^お|^[^\p{Han}]*\p{Han}[^\p{Han}]*$')


def extract(results: List[SpecificKeyword], parse_results, data):
    combine_set = set()
    target = None

    for line, tokens in parse_results:

        for face, data in tokens:
            if data[0] != '名詞':
                continue
            if target is not None and data[2] == 'サ変接続' and face != "議論" and sahen_blockpattern.search(face) is None:

                combine_set.add((target, face,))

            if data[1] == '一般' and not meishi_blockpattern.search(face):

                target = face

    new_results = []

    for headword, subword in combine_set:
        if headword in results:
            if subword in results:
                continue

            exist_index = results.index(headword)
            exist_word = results[exist_index]

            if len(headword) > len(exist_word.headword):
                exist_word.headword = headword
            if subword not in exist_word.subwords:
                exist_word.add_subword(subword)

        else:
            new_results.append(SpecificKeyword(
                headword=headword, subwords=[subword]))

    results.extend(new_results)

    return results
