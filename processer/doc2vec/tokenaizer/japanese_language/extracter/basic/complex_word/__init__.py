

from collections import defaultdict, deque


from typing import DefaultDict, Deque, Dict, List

from sklearn import base


from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re


from doc2vec.components.japanese_language.rule import symbol_not_bracket
from doc2vec.components.japanese_language.rule.usual_and_sahen import check_ususal_and_sahen
from doc2vec.components.japanese_language.rule.valid_noun_jp import check_valid_noun
from doc2vec.components.japanese_language.regex_patterns import kanji_only
from doc2vec.components.japanese_language.regex_patterns import hiragana_include


eiji_pt = re.compile(r'^[\w]+$', re.A)
kigou = re.compile(r'^\W+$')
kuuhaku = re.compile(r'\s+')
hiragana_pt = re.compile(r'[\p{Hiragana},。、]')
hiragana_itimoji_pt = re.compile(r'\p{Hiragana}{2}')
式と型 = {'式', '型'}
目的修飾語 = {'用', '専用', '等'}
辞書に収録されている元号 = {'昭和', '平成', '明治', '大正'}


class Context:
    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.chunk = []
        self.force_headword = False
        self.chunklen = 0

    def append_token(self, face, data):
        self.chunk.append((face, data,))
        self.chunklen += 1

    def extend_face(self, faces):
        self.chunk.extend(faces)
        self.chunklen += len(faces)


def extract(results: List[SpecificKeyword], parse_results: List, data):

    complexword_set = set()
    context = Context()
    context.chunklen = 0
    word_to_linenumber = defaultdict(deque)
    force_headword_map = {}

    line_number = -1
    for line, tokens in parse_results:

        _add_to_complexword_set(
            complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
        line_number += 1
        for face, data in tokens:
            if hiragana_include.pattern.search(face):

                _add_to_complexword_set(
                    complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
                continue

            if symbol_not_bracket.check_symbol(face=face) == True:
                if symbol_not_bracket.check_is_breaktoken(data=data) == True:
                    _add_to_complexword_set(
                        complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)

                    continue

            if data[0] == "接頭詞" or face[0] == '御':
                _add_to_complexword_set(
                    complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
                continue
            if data[1] == "代名詞" or data[1] == "副詞可能" or data[0] == "副詞":
                _add_to_complexword_set(
                    complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
                continue
            context.append_token(face=face, data=data)

    _add_to_complexword_set(
        complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)

    reguraized_complexwords = []

    for complexword in complexword_set:
        index = 0
        is_marged = False
        while index < len(reguraized_complexwords):

            reguraized_complexword = reguraized_complexwords[index]

            if complexword in reguraized_complexword:
                is_marged = True
                word_to_linenumber[reguraized_complexword].extend(
                    word_to_linenumber[complexword])
            if reguraized_complexword in complexword:
                is_marged = True
                word_to_linenumber[complexword].extend(
                    word_to_linenumber[reguraized_complexword])
                reguraized_complexwords[index] = complexword

            index += 1
        if is_marged == False:
            reguraized_complexwords.append(complexword)

    for complexword in reguraized_complexwords:
        if complexword in results:
            continue

        results.append(SpecificKeyword(
            headword=complexword, line_numbers=word_to_linenumber[complexword], is_fixed_headword=force_headword_map[complexword]))

    return results


datetime_kanji_pattern = re.compile(r'[年月日時分秒]$')


def _check_and_split_context(context: Context):
    if context.chunklen <= 1:

        return False
    face, data = context.chunk[-1]
    if face in 目的修飾語 or (data[1] == "接尾" and (data[2] == "助数詞" or data[2] == "形容動詞語幹")):

        return False
    is_keep_number = False
    index = -1
    limit = context.chunklen - 1
    number_index_list = []
    number_start_index = None

    while index < limit:
        index += 1
        face, data = context.chunk[index]

        is_number_exist = data[1] == "数" or data[2] == "助数詞" or (
            data[1] != '固有名詞' and datetime_kanji_pattern.search(face) != None and face not in 辞書に収録されている元号)
        if index > 0:
            is_number_exist |= "".join(
                [r[0] for r in context.chunk[index - 1: index + 1]]) == "令和"
        if is_keep_number == False and is_number_exist == True:
            number_start_index = index
        if is_keep_number == True and is_number_exist == False:
            number_index_list.append((number_start_index, index))
            number_start_index = None
        is_keep_number = is_number_exist
    if is_keep_number == True:
        number_index_list.append((number_start_index, index))
    if len(number_index_list) == 0:
        return [context.chunk]
    split_index_list = []

    for start, end in number_index_list:
        if start == 0 and (end == context.chunklen - 1 or (end == context.chunklen - 2 and context.chunk[-1][0] in 式と型)):
            return False

        is_after_chunk_exist = end < context.chunklen - 1
        if is_after_chunk_exist == False or context.chunk[end + 1][0] not in 式と型:
            split_index_list.append((start, end,))
    split_cursor = 0
    split_index_list_len = len(split_index_list)
    if split_index_list_len > 0:

        start, end = split_index_list[split_cursor]
        split_cursor += 1
    else:
        start = end = context.chunklen

    subchunks = []
    subchunk = []
    while index < limit:
        index += 1
        if index >= start:
            if index <= end:
                continue
            if len(subchunk) > 0:
                subchunks.append(subchunk)
            subchunk = []

            split_cursor += 1
            if split_cursor < split_index_list_len:
                start, end = split_index_list[split_cursor]
            else:
                start = end = context.chunklen
        face, data = context.chunk[index]
        subchunk.append((face, data, ))
    if len(subchunk) > 0:
        subchunks.append(subchunk)

    return subchunks


def _add_to_complexword_set(complexword_set: set, context: Context, word_to_linenumber: DefaultDict[str, set], line_number, force_headword_map: Dict):
    check_result = _check_and_split_context(context=context)

    if check_result == False:
        context.clear()
        return
    for subchunk in check_result:
        if len(subchunk) == 1:
            continue
        word = ''.join([token[0] for token in subchunk])
        word_to_linenumber[word].append(line_number)
        complexword_set.add(word)
        force_headword_map[word] = subchunk[0][1][1] != "サ変接続"
    context.clear()
