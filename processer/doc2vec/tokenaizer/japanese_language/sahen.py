from typing import Dict, List
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
            if target is not None and data[1] == 'サ変接続' and face != "議論" and sahen_blockpattern.search(face) is None:
                check_pt = re.compile('[\p{Hiragana}、]' + target)
                if check_pt.search(line):
                    combine_set.add((target, face,))

            if data[1] == '一般' and not meishi_blockpattern.search(face):

                target = face

    new_results = []
    head2word: Dict[SpecificKeyword] = {}

    for headword, subword in combine_set:

        if headword in head2word:

            if subword in results:
                continue

            clone: SpecificKeyword = head2word[headword].clone()
            clone.add_subword(subword=subword)
            new_results.append(clone)
            continue

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
