

from collections import defaultdict, deque


from typing import DefaultDict, Deque, Dict, List


from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re

from doc2vec.tokenaizer.japanese_language.extracter.components.rule import symbol_not_bracket
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.usual_and_sahen import check_ususal_and_sahen
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.valid_noun_jp import check_valid_noun
from doc2vec.tokenaizer.japanese_language.extracter.components.regex_patterns import kanji_only
from doc2vec.tokenaizer.japanese_language.extracter.components.regex_patterns import hiragana_only

from ...components.regex_patterns.hiragana_2or1 import hiragana_2or1_pt


eiji_pt = re.compile(r'^[\w]+$', re.A)
kigou = re.compile(r'^\W+$')
kuuhaku = re.compile(r'\s+')
hiragana_pt = re.compile(r'[\p{Hiragana},。、]')
hiragana_itimoji_pt = re.compile(r'\p{Hiragana}{2}')
式と型 = {'式', '型'}
目的修飾語 = {'用', '専用'}


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
            if hiragana_only.pattern.search(face):

                _add_to_complexword_set(
                    complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
                continue
            if data[1] == "接尾" and face not in 式と型 and face != '用':

                context.append_token(face=face, data=data)

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
            if data[1] == "代名詞" or data[1] == "副詞可能":
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

        results.append(SpecificKeyword(
            headword=complexword, line_numbers=word_to_linenumber[complexword], is_fixed_headword=force_headword_map[complexword]))

    return results


datetime_kanji_pattern = re.compile(r'[年月日時分秒]$')


def _check_context(context: Context):
    if context.chunklen <= 1:

        return False
    face, data = context.chunk[-1]
    if face in 目的修飾語 or (data[1] == "接尾" and (data[2] == "助数詞" or data[2] == "形容動詞語幹")):

        return False
    is_number_only = True
    for face, data in context.chunk:
        is_number_only &= data[1] == "数" or data[2] == "助数詞" or (
            data[1] != '固有名詞' and datetime_kanji_pattern.search(face) != None)
    if is_number_only == True:
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
