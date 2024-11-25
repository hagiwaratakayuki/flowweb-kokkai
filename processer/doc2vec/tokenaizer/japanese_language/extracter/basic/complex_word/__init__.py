

from collections import defaultdict, deque
from operator import is_not
from re import L
from typing import DefaultDict, Deque, Dict, List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re

from doc2vec.tokenaizer.japanese_language.extracter.components.rule import symbol_not_bracket
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.usual_and_sahen import check_ususal_and_sahen
from doc2vec.tokenaizer.japanese_language.extracter.components.rule.valid_noun_jp import check_valid_noun

from ...components.regex_patterns.hiragana_2or1 import hiragana_2or1_pt


eiji_pt = re.compile(r'^[\w]+$', re.A)
kigou = re.compile(r'^\W+$')
kuuhaku = re.compile(r'\s+')
hiragana_pt = re.compile(r'[\p{Hiragana},。、]')
hiragana_itimoji_pt = re.compile(r'\p{Hiragana}{2}')
式と型 = set(['式', '型'])


class Context:
    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.chunk = []
        self.force_headword = False
        self.chunklen = 0

    def append_face(self, face):
        self.chunk.append(face)
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
        line_number += 1
        if context.chunklen > 1:
            _add_to_complexword_set(
                complexword_set=complexword_set, context=context, line_number=line_number, word_to_linenumber=word_to_linenumber, force_headword_map=force_headword_map)
        else:
            context.clear()

        if isinstance(tokens, list) == False:
            tokens = list(tokens)
        len_tokens = len(tokens)
        index = -1
        while index < len_tokens - 1:
            index += 1
            face, data = tokens[index]

            if data[0] == '接頭詞':
                context.clear()
                continue
            if data[2] == '形容動詞語幹':

                context.clear()

                continue
            if data[2] == '数助詞':
                if context.chunklen > 1:
                    context.append(face)

                continue

            if eiji_pt.search(face) is not None:

                context.append_face(face=face)
                continue
            if data[1] == '数':
                if index == len_tokens - 1:
                    if context.chunklen > 1:
                        context.append(face)
                    continue

                subchunk = []
                is_add_chunk = True
                for subindex in range(index + 1, len_tokens):
                    subface, subdata = tokens[subindex]
                    if eiji_pt.search(subface) is not None or subdata[1] == '数':
                        subchunk.append(subface)
                        continue
                    if (subdata[1] == '数助詞' and subface not in 式と型) or data[2] == '形容動詞語幹':
                        is_add_chunk = False
                        index = subindex
                        break
                    if symbol_not_bracket.check_symbol(face=subface) == True:
                        if symbol_not_bracket.check_is_bracket(data=data) == True:
                            is_add_chunk = len(subchunk) > 1
                            index = index
                            break
                        else:
                            subchunk.append(face)

                    if subdata[1] != '名詞' or check_ususal_and_sahen(subdata) == False or check_valid_noun(subface) == False:
                        index = subindex - 1

                        break
                if is_add_chunk:
                    context.extend_face(subchunk)

                continue
            if symbol_not_bracket.check_symbol(face=face) == True:

                if context.chunklen > 1:

                    if symbol_not_bracket.check_is_bracket(data=data):
                        _add_to_complexword_set(
                            complexword_set=complexword_set, context=context, word_to_linenumber=word_to_linenumber, line_number=line_number, force_headword_map=force_headword_map)

                    else:
                        context.append_face(face=face)
                continue

            if check_valid_noun(face) == False:
                if context.chunklen > 1:
                    _add_to_complexword_set(complexword_set=complexword_set, context=context,
                                            word_to_linenumber=word_to_linenumber, line_number=line_number, force_headword_map=force_headword_map)
                else:
                    context.clear()
                continue
            if data[0] == '名詞' and check_ususal_and_sahen(data=data):
                context.append_face(face)
                continue
            if data[0] == '名詞' and data[1] == '接尾' and data[2] == '一般' and context.chunklen > 1:
                context.append_face(face)
                context.force_headword = True
                continue
            if face == '問題' and context.chunklen > 1:
                context.append_face('問題')
                continue

            if context.chunklen > 1:
                _add_to_complexword_set(
                    complexword_set=complexword_set, context=context, word_to_linenumber=word_to_linenumber, line_number=line_number, force_headword_map=force_headword_map)
            else:
                context.clear()

    if context.chunklen > 1:
        _add_to_complexword_set(complexword_set=complexword_set, context=context,
                                word_to_linenumber=word_to_linenumber, line_number=line_number, force_headword_map=force_headword_map)

    for complexword in complexword_set:
        print('complex:', complexword)
        if complexword in results:
            continue
        results.append(SpecificKeyword(
            headword=complexword, line_numbers=word_to_linenumber[complexword], is_fixed_headword=force_headword_map[complexword]))

    return results


def _add_to_complexword_set(complexword_set: set, context: Context, word_to_linenumber: DefaultDict[str, set], line_number, force_headword_map: Dict):
    word = ''.join(context.chunk)
    word_to_linenumber[word].append(line_number)
    complexword_set.add(word)
    force_headword_map[word] = context.force_headword
    context.clear()
