

from collections import defaultdict, deque


from typing import DefaultDict, Deque, Dict, List


from doc2vec.util.specified_keyword import SpecifiedKeyword
import regex as re


from doc2vec.components.japanese_language.rule import symbol_not_bracket
from doc2vec.components.japanese_language.regex_patterns import hiragana_include
from doc2vec.components.japanese_language.regex_patterns import noun_blockpattern


eiji_pt = re.compile(r'^[\w]+$', re.A)
kigou = re.compile(r'^\W+$')


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

    def pop_chunk(self):
        self.chunk.pop()
        self.chunklen -= 1

    def append_token(self, face, data):
        self.chunk.append((face, data,))
        self.chunklen += 1

    def extend_face(self, faces):
        self.chunk.extend(faces)
        self.chunklen += len(faces)


def extract(results: List[SpecifiedKeyword], parse_results: List, data):

    complexword_set = set()
    context = Context()

    word_to_linenumber = defaultdict(deque)
    force_headword_map = {}

    line_number = -1
    for line, tokens in parse_results:

        _add_to_complexword_set(
            complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
        line_number += 1
        for face, data in tokens:
            if face != '子ども' and hiragana_include.pattern.search(face) is not None or noun_blockpattern.compiled.search(face) is not None:

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

        results.append(SpecifiedKeyword(
            headword=complexword, tokens=word_to_linenumber[complexword], is_fixed_headword=force_headword_map[complexword]))

    return results


datetime_kanji_pattern = re.compile(r'[年月日時分秒]$')

# todo 助数詞が入る場合のみカットするように


def _check_context(context: Context):
    if context.chunklen <= 1:

        return False
    if context.chunk[-1][0] == "化":
        context.pop_chunk()

        if context.chunklen <= 1:

            return False
    face, data = context.chunk[-1]
    if face in 目的修飾語 or (data[1] == "接尾" and (data[2] == "助数詞" or data[2] == "形容動詞語幹")):

        return False
    is_keep_number = False
    index = -1
    limit = context.chunklen - 1
    latest_number_token = None
    latest_number_index = -1
    is_number_only = True

    while index < limit:
        index += 1

        face, data = context.chunk[index]

        is_keep_number = data[1] == "数" or data[2] == "助数詞" or (
            data[1] != '固有名詞' and datetime_kanji_pattern.search(face) != None and face not in 辞書に収録されている元号)
        if index > 0:
            is_keep_number |= "".join(
                [r[0] for r in context.chunk[index - 1: index + 1]]) == "令和"
        is_number_only &= is_keep_number
        if is_number_only == True:
            latest_number_token = (face, data,)
            latest_number_index = index

    if is_number_only == True:
        return False
    if latest_number_token is not None:

        face, data = latest_number_token
        if data[2] == "助数詞" and face not in 式と型:
            context.chunk = context.chunk[latest_number_index + 1:]
            if len(context.chunk) <= 1:
                return False
    face, data = context.chunk[-1]
    if data[2] == "助数詞" and face not in 式と型:
        return False
    return True


def _add_to_complexword_set(complexword_set: set, context: Context, word_to_linenumber: DefaultDict[str, set], line_number, force_headword_map: Dict):

    if _check_context(context=context) == False:
        context.clear()
        return

    word = ''.join([token[0] for token in context.chunk])
    word_to_linenumber[word].append(line_number)
    complexword_set.add(word)
    force_headword_map[word] = context.chunk[0][1][1] != "サ変接続"
    context.clear()
