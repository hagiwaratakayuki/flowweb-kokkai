from collections import defaultdict, deque

from typing import Deque, Dict, List

from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re


from doc2vec.components.japanese_language.rule.symbol_not_bracket import check_is_breaktoken, check_symbol, check_symbol_without_bracket
from doc2vec.components.japanese_language.rule.valid_noun_jp import check_valid_noun
from doc2vec.components.japanese_language.rule.usual_and_sahen import check_ususal_and_sahen
from doc2vec.components.japanese_language.regex_patterns import hiragana_include
from doc2vec.components.japanese_language.regex_patterns import noun_blockpattern

eiji = re.compile(r'^\w+$', re.A)
kigou = re.compile(r'^\W+$')

sahen_blockpattern = re.compile('^お')
一般と固有名詞 = {'一般', '固有名詞'}
目的修飾接尾語 = {'専用'}


class Context:
    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.noun = None
        self.index = -2
        self.pending = None

    def set_noun(self, noun, index):
        self.noun = noun
        self.index = index

    def set_pending_noun(self, noun, index):
        self.pending = (noun, index,)

    def clear_pending(self):
        self.pending = None

    def use_pending(self, additional_face=''):
        noun, index = self.pending
        noun += additional_face
        self.set_noun(noun=noun, index=index)
        self.clear_pending()


def extract(results: List[SpecificKeyword], parse_results, data):

    line_number = -1
    noun_sahen = defaultdict(set)
    context = Context()
    for line, tokens in parse_results:
        context.clear()
        line_number += 1

        tokens_list = list(tokens)
        lentokens = len(tokens)
        index = -1
        for face, data in tokens:

            index += 1
            if context.pending != None:
                if face in "編章条項節款目":
                    context.use_pending(face)
                else:
                    context.clear_pending()

                continue
            if data[2] == '形容動詞語幹':
                if context.index + 1 == index:
                    context.clear()
                continue
            if check_symbol(face=face):
                if context.noun == None and check_is_breaktoken(data=data) == False:
                    context.set_noun(face, index)
                continue

            if data[1] == '数':
                context.set_pending_noun(face, index)
                continue
            if eiji.search(face) is not None:

                context.set_noun(face, index)
                continue

            if data[0] == '名詞' and data[1] in 一般と固有名詞 and check_valid_noun(face=face) == True and hiragana_include.pattern.search(face) == None:

                context.set_noun(face, index)
                continue
            if context.noun is not None and data[1] == 'サ変接続' and sahen_blockpattern.search(face) is None and face != "専用":
                is_pass = False

                # 「○○用」「○○○専用」といった目的修飾的な用法を判定
                # サ変 + 接尾と「○○○専用」を排除
                next_index = index + 1
                if next_index < lentokens:
                    next_face, next_data = tokens_list[next_index]
                    if next_data[1] == "接尾":

                        continue
                    if next_face in 目的修飾接尾語:
                        continue

                k = (context.noun, face,)

                noun_sahen[k].add(line_number)

    # 複合語チェック(サ変接続)
    # 複合語チェック(名詞)
    # サブワードリンクチェック
    # 元の特定語と現在のペアから新しいリストを生成
    new_results = []

    empty_set = set()
    keys = list(noun_sahen.keys())

    new_results: Deque[SpecificKeyword] = deque()

    additional_results = deque()

    for key in keys:

        line_numbers = noun_sahen[key]
        noun, sahen = key

        for keyword_obj in results:

            if keyword_obj == noun:

                inter = keyword_obj.line_numbers & line_numbers

                if inter == empty_set:

                    continue
                if keyword_obj.is_allow_add_multiple_subword == True or len(keyword_obj.subwords) == 0:

                    new_keyword_obj = keyword_obj.clone()
                    new_keyword_obj.clear_subword()
                    new_keyword_obj.add_subword(sahen)
                    new_keyword_obj.line_numbers = inter

                    additional_results.append(new_keyword_obj)
                    keyword_obj.line_numbers -= inter
                    noun_sahen[key] -= inter
        results.extend(additional_results)
        additional_results = deque()
    keys = [k for k, ln in noun_sahen.items() if ln != empty_set]

    for keyword_obj in results:

        for key in keys:

            line_numbers = noun_sahen[key]
            noun, sahen = key

            inter = keyword_obj.line_numbers & line_numbers

            if inter == empty_set:
                continue

            if keyword_obj == sahen:

                noun_sahen[key] -= inter
                if keyword_obj.is_fixed_headword == False:

                    position = keyword_obj.index_of(sahen)
                    if position == 0:
                        keyword_obj.line_numbers -= inter
                        noun_sahen[(noun, keyword_obj.headword,)] = inter

        if keyword_obj.line_numbers != empty_set:

            new_results.append(keyword_obj)

    additional_kws = deque()
    keys = [k for k, ln in noun_sahen.items() if ln != empty_set]

    for keyword_obj in new_results:

        for key in keys:

            line_numbers = noun_sahen[key]
            noun, sahen = key

            inter = keyword_obj.line_numbers & line_numbers

            if inter == empty_set:
                continue
            if keyword_obj.is_allow_add_multiple_subword == True:
                try:

                    subword_link_index = keyword_obj.subwords.index(noun)
                    noun_sahen[key] -= inter
                    if subword_link_index < len(keyword_obj.subwords) - 1:
                        new_keword_obj = keyword_obj.clone()
                        new_keword_obj.clear_subword()
                        new_subword = keyword_obj.subwords[:subword_link_index + 1] + [
                            sahen]
                        new_keword_obj.add_subword(new_subword)
                        additional_kws.append(new_keword_obj)
                    else:
                        keyword_obj.add_subword(sahen)
                except:
                    continue

    new_results.extend(additional_kws)
    new_results = [r for r in new_results if r.line_numbers != empty_set]
    keys = [k for k, ln in noun_sahen.items() if ln != empty_set]
    for key in keys:
        if noun_sahen[key] == empty_set:
            continue
        noun, sahen = key

        new_results.append(SpecificKeyword(headword=noun, subwords=[sahen]))

    return new_results
