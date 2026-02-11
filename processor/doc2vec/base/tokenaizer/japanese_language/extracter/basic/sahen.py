from collections import defaultdict, deque

from turtle import position
from typing import Deque, Dict, List, OrderedDict
from xml.etree.ElementInclude import include

from numpy import Infinity

from doc2vec.util.specified_keyword import EqIn, SpecifiedKeyword
import regex as re


from doc2vec.components.japanese_language.rule.symbol_not_bracket import check_is_breaktoken, check_symbol, check_symbol_without_bracket
from doc2vec.components.japanese_language.rule.valid_noun_jp import check_valid_noun

from doc2vec.components.japanese_language.regex_patterns import hiragana_include


eiji = re.compile(r'^\w+$', re.A)
kigou = re.compile(r'^\W+$')

sahen_blockpattern = re.compile('^お')
一般と固有名詞 = {'一般', '固有名詞'}
目的修飾接尾語 = {'専用'}


class Context:
    def __init__(self) -> None:
        self.clear()
        self.noun_sahens = defaultdict(set)
        self.line_number = -1

    def clear(self):
        self.noun = None
        self.index = -2
        self.pending = None

        self._clear_sahens()

    def check_and_clear(self):
        self.check_sahens()
        self.clear()

    def _clear_sahens(self):

        self.sahens = []
        self.is_sahen_add = False

    def add_sahen(self, sahen):
        self.sahens.append(sahen)
        self.is_sahen_add = True

    def set_noun(self, noun, index):

        self._check_and_clear_sahens()
        self.noun = noun
        self.index = index

    def check_sahens(self):
        is_sahen_add = self.is_sahen_add
        sahens = self.sahens
        noun = self.noun

        if (is_sahen_add == True):
            self.noun_sahens[(noun, tuple(sahens))].add(self.line_number)

    def _check_and_clear_sahens(self):

        self.check_sahens()
        self._clear_sahens()

    def set_pending_noun(self, noun, index):
        self.pending = (noun, index,)

    def clear_pending(self):
        self.pending = None

    def use_pending(self, line_number, additional_face=''):
        noun, index = self.pending
        noun += additional_face
        ret = self.set_noun(noun=noun, index=index)
        self.clear_pending()
        return ret


def extract(results: List[SpecifiedKeyword], parse_results, data):

    noun_sahens = defaultdict(set)
    context = Context()
    for line, tokens in parse_results:
        context.check_and_clear()

        context.line_number += 1

        tokens_list = list(tokens)
        lentokens = len(tokens)
        index = -1
        for face, data in tokens:

            index += 1
            if context.pending != None:
                if face in "編章条項節款目":
                    key = context.use_pending(face)

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

            if len(face) != 1 and data[0] == '名詞' and data[1] in 一般と固有名詞 and check_valid_noun(face=face) == True and hiragana_include.pattern.search(face) == None:

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

                context.add_sahen(face)
    context.check_sahens()
    noun_sahens = context.noun_sahens

    # 行が重なっているかどうか確認
    #  サ変が含まれるか確認　候補選定
    #  もう一度ループ
    #  候補に確認
    #  もう一度ループ
    # 　名詞が含まれるか確認　→　サ変がどれだけ含まれるか確認してカット
    next_results = []

    empty_set = set()

    canditate_index = []
    canditates_listmap: List[Deque] = []
    next_results: List[SpecifiedKeyword] = []
    keys = list(noun_sahens.keys())

    for key in keys:

        for keyword_obj in results:
            # print(keyword_obj.headword, keyword_obj.line_numbers)
            line_numbers = noun_sahens[key]

            inter = keyword_obj.tokens & line_numbers

            if inter == empty_set:

                continue
            noun, sahens = key

            is_sahens_include = False
            not_includes = deque()
            top_position = Infinity
            is_end = False
            for sahen in sahens:
                sahen_index = keyword_obj.index_of(sahen)
                is_include = sahen_index != -1

                is_sahens_include |= is_include
                if is_include == False:
                    not_includes.append(sahen)
                elif top_position > sahen_index:
                    top_position = sahen_index
                if sahen_index + len(sahen) == keyword_obj.get_headword_length():
                    is_end == True

            if is_sahens_include == True:

                noun_sahens[key] -= inter

                if keyword_obj.is_fixed_headword == False:

                    if top_position == 0 or is_end == True:
                        keyword_obj.tokens -= inter
                        new_key = (noun, (keyword_obj.headword,) +
                                   tuple(not_includes), )
                        noun_sahens[new_key] = inter
                        canditate_index.append(EqIn(keyword_obj.headword))
                        canditates = deque()
                        canditates.append(new_key)
                        canditates_listmap.append(canditates)

    is_remain_candiates = True
    noun_sahens = {key: line_numbers for key,
                   line_numbers in noun_sahens.items() if line_numbers != empty_set}

    while is_remain_candiates == True:
        is_remain_candiates = False
        linked_line_numbers_dict = defaultdict(set)
        next_noun_sahens = {}
        for key, line_numbers in noun_sahens.items():

            noun, sahens = key

            try:

                index = canditate_index.index(noun)

                target_keys = list(canditates_listmap[index])
                next_target_keys = deque()
                for target_key in target_keys:
                    if target_key == key or target_key not in noun_sahens:

                        continue

                    inter = line_numbers & noun_sahens[target_key]

                    if inter == empty_set:
                        continue

                    target_noun, target_sahens = target_key

                    add_sahens = [
                        sahen for sahen in sahens if sahen not in target_sahens]
                    new_target_sahens = target_sahens + tuple(add_sahens)
                    new_key = (target_noun, new_target_sahens, )
                    next_noun_sahens[new_key] = inter

                    next_target_keys.append(new_key)
                    for add_sahen in add_sahens:
                        try:
                            _index = canditate_index.index(add_sahen)
                            _target_keys = canditates_listmap[_index]
                            _target_keys.append(new_key)
                        except ValueError:
                            canditate_index.append(EqIn(add_sahen))
                            canditates = deque()
                            canditates.append(new_key)
                            canditates_listmap.append(canditates)

                    linked_line_numbers_dict[key].update(inter)
                    linked_line_numbers_dict[target_key].update(inter)

                    is_remain_candiates = True
                canditates_listmap[index].extend(next_target_keys)

            except ValueError:

                pass

            next_noun_sahens[key] = line_numbers

        noun_sahens = {key: line_numbers - linked_line_numbers_dict[key] for key,
                       line_numbers in next_noun_sahens.items() if line_numbers != linked_line_numbers_dict[key]}

    next_results = []

    items = [(key, line_numbers,) for key,
             line_numbers in noun_sahens.items() if line_numbers != empty_set]

    for keyword_obj in results:

        for key, line_numbers in items:
            inter = keyword_obj.tokens & line_numbers

            if inter == empty_set:

                continue
            noun, sahens = key

            if keyword_obj == noun:

                if keyword_obj.is_allow_add_multiple_subword == True or len(keyword_obj.subwords) == 0:

                    new_keyword_obj = keyword_obj.clone()
                    new_keyword_obj.add_subword(sahens)
                    new_keyword_obj.tokens = inter

                    next_results.append(new_keyword_obj)
                    keyword_obj.tokens -= inter
                    noun_sahens[key] -= inter
            else:
                is_connectable = False

                for subword in keyword_obj.subwords:
                    is_connectable |= noun in subword
                    if is_connectable == True:
                        break
                if is_connectable and (keyword_obj.is_allow_add_multiple_subword == True or len(keyword_obj.subwords) == 0):
                    new_keyword_obj = keyword_obj.clone()
                    new_keyword_obj.add_subword(sahens)
                    new_keyword_obj.tokens = inter

                    next_results.append(new_keyword_obj)
                    keyword_obj.tokens -= inter
                    noun_sahens[key] -= inter

        if keyword_obj.tokens != empty_set:
            next_results.append(keyword_obj)

    for key in noun_sahens:

        if noun_sahens[key] == empty_set:
            continue
        noun, sahens = key

        next_results.append(SpecifiedKeyword(headword=noun, subwords=sahens))

    return next_results
