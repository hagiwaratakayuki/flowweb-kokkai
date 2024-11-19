from typing import Dict, List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re
meishi_blockpattern = re.compile(r'[所々\W]+$')
sahen_blockpattern = re.compile(
    '^[\W\p{Katakana}]+$|^お|^[^\p{Han}]*\p{Han}[^\p{Han}]*$')


def extract(results: List[SpecificKeyword], parse_results, data):
    combine_set = set()
    target = None

    weightings = []

    is_meishirennzoku = False
    is_force_split = False
    for line, tokens in parse_results:
        is_meishirennzoku = False

        if len(weightings) > 0:
            combine_set.add((target, tuple(weightings)))
        target = None
        weightings = []
        for face, data in tokens:

            if data[0] != '名詞' or data[1] == '代名詞':
                is_meishirennzoku = False
                if len(weightings) > 0:
                    combine_set.add((target, tuple(weightings)))
                target = None
                weightings = []
                continue
            if target is not None and data[1] == 'サ変接続' and sahen_blockpattern.search(face) is None:

                if (target + face) not in line:

                    weightings.append(face)

            if data[1] == '一般' and not meishi_blockpattern.search(face):
                if is_meishirennzoku == True:
                    weightings.append(face)
                else:

                    target = face

    new_results = []
    head2word: Dict[str, SpecificKeyword] = {}

    for headword, subword in combine_set:

        if headword in results:

            if subword in results:
                continue

            exist_index = results.index(headword)
            exist_word = results[exist_index]
            head2word[headword] = exist_word.clone()

            if len(headword) > len(exist_word.headword):
                exist_word.headword = headword

            if subword not in exist_word.subwords:

                exist_word.add_subword(subword)

        else:
            new_result = SpecificKeyword(
                headword=headword, subwords=[subword])
            new_results.append(new_result)

    results.extend(new_results)

    return results
