from collections import defaultdict
import keyword
from os import remove
from typing import Dict, List

from httpx import delete
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re

from doc2vec.tokenaizer.japanese_language.extracter.components.rule.symbol_not_bracket import check_is_bracket, check_symbol, check_symbol_without_bracket
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.valid_noun_jp import check_valid_noun
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.usual_and_sahen import check_ususal_and_sahen
from ..components.regex_patterns.hiragana_2or1 import hiragana_2or1_pt

eiji = re.compile(r'^\w+$', re.A)
kigou = re.compile(r'^\W+$')
meishi_blockpattern = re.compile(r'[所々様]$')
sahen_blockpattern = re.compile('^お')
一般と固有名詞 = {'一般', '固有名詞'}


def extract(results: List[SpecificKeyword], parse_results, data):
    combine_set = set()

    line_number = -1
    noun_sahen = defaultdict(set)
    for line, tokens in parse_results:
        noun = None
        line_number += 1
        index = -1

        for face, data in tokens:

            index += 1

            if data[1] != '名詞':
                continue

            if data[2] == '形容動詞語幹':
                noun = None
            if check_symbol(face=face):
                if noun == None and check_is_bracket(data=data) == False:
                    noun = face
                continue
            if noun == None and eiji.search(face) is not None:
                noun = face
                continue
            if data[0] == '名詞' and data[1] in 一般と固有名詞 and check_valid_noun(face=face) == True:
                noun = face
            if noun is not None and data[1] == 'サ変接続' and sahen_blockpattern.search(face):
                k = (noun, face,)
                noun_sahen[k].add(line_number)

    # todo ここから複合語と法律用語にサ変接続を付け加えていく
    # 　複合語にサ変が含まれるものを取り出し。法律などの強制的に主語(?)になりうるものでないのを確認。最初の単語がサ変ならば名詞＋サ変としてペアに設定。以降の名詞によるペアを削除
    # 　名詞が含まれるものを取得。サ変を追加。　
    new_results = []

    empty_set = set()
    keys = list(noun_sahen.keys())
    least_line_numbers = defaultdict(set)

    index_to_key = defaultdict(set)
    deleted_keys = {}
    newpaire_map = defaultdict(lambda: defaultdict(set))

    for i, keyword_obj in enumerate(results):

        for key in keys:
            line_numbers = noun_sahen[key]
            noun, sahen = key
            inter = keyword_obj.line_numbers & line_numbers

            if inter == empty_set:
                continue
            least_line_numbers[key].update(inter)
            if keyword_obj == sahen:

                if keyword_obj.is_fixed_headword == True:

                    is_delete_key = line_numbers == least_line_numbers[key]

                else:
                    position = keyword_obj.index_of(sahen)
                    if position == 0:

                        newpaire_map[key][keyword_obj.headword].update(inter)

                    is_delete_key = line_numbers == least_line_numbers[key]

            if keyword_obj == noun:
                index_to_key[i].add((key, inter))
                is_delete_key = line_numbers == least_line_numbers[key]
            if deleted_keys.get(key, False) == True:
                continue
            if is_delete_key == True:
                deleted_keys[key] = True

    # サ変を追加する作業ここから

    for i, keyword_obj in enumerate(results):

        least_line_numbers = keyword_obj.line_numbers
        for key in index_to_key.get(i, []):
            for new_subword, line_numbers in newpaire_map[key].items():
                inter = keyword_obj.line_numbers & line_numbers
                least_line_numbers -= inter
                noun_sahen[key] -= inter
                if inter == empty_set:
                    continue

                new_obj = keyword_obj.clone()
                new_obj.add_subword(new_subword)
                new_results.append(new_obj)
        if least_line_numbers != empty_set:
            new_results.append(keyword_obj)
    for key, line_numbers in noun_sahen.items():
        if key in deleted_keys or line_numbers == empty_set:
            continue
        noun, sahen = key
        new_results.append(SpecificKeyword(headword=noun, subwords=[sahen]))

    return new_results
