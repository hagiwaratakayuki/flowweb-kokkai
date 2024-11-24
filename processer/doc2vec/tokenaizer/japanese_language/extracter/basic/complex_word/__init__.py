

from collections import defaultdict, deque
from operator import is_not
from re import L
from typing import DefaultDict, Deque, List
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


def extract(results: List[SpecificKeyword], parse_results: List, data):
    complexword_set = set()
    chunk = []
    chunklen = 0
    word_to_linenumber = defaultdict(deque)

    line_number = -1
    for tokens, data in parse_results:
        line_number += 1
        if chunklen > 1:
            _add_to_complexword_set(
                complexword_set=complexword_set, chunk=chunk, line_number=line_number, word_to_linenumber=word_to_linenumber)
        chunk = []
        chunklen = 0
        if isinstance(tokens, list) == False:
            tokens = list(tokens)
        len_tokens = len(tokens)
        index = -1
        while index < len_tokens - 1:
            index += 1
            face, data = tokens[index]
            chunklen = len(chunk)

            if data[0] == '接頭詞':
                chunk = []
                continue
            if data[2] == '形容動詞語幹':

                chunk = []

                continue
            if data[2] == '数助詞':
                if chunklen > 1:
                    _add_to_chunk(face=face, chunk=chunk)

                continue

            if eiji_pt.search(face) is not None:
                _add_to_chunk(chunk=chunk, face=face)
                continue
            if data[1] == '数':
                if index == len_tokens - 1:
                    if chunklen > 1:
                        _add_to_chunk(face, chunk)
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
                    _add_to_chunk(face=face, chunk=chunk)
                continue
            if symbol_not_bracket.check_symbol(face=face) == True:
                if chunklen > 1:

                    if symbol_not_bracket.check_is_bracket(face):
                        _add_to_complexword_set(
                            complexword_set=complexword_set, chunk=chunk, word_to_linenumber=word_to_linenumber, line_number=line_number)
                        chunk = []

                    else:
                        _add_to_chunk(face=face, chunk=chunk)
                continue

            if check_valid_noun(face) == False:
                if chunklen > 1:
                    _add_to_complexword_set(chunk=chunk)
                chunk = []
                continue
            if data[0] == '名詞' and (data[1] == '一般' or data[1] == 'サ変接続'):
                _add_to_chunk(face, chunk)
                continue
            if face == '問題' and chunklen > 1:
                _add_to_chunk('問題', chunk=chunk)
                continue
            if chunklen > 1:
                _add_to_complexword_set(
                    complexword_set=complexword_set, chunk=chunk, word_to_linenumber=word_to_linenumber, line_number=line_number)
            chunk = []

    chunklen = len(chunk)
    if chunklen > 1:
        _add_to_complexword_set(complexword_set=complexword_set, chunk=chunk,
                                word_to_linenumber=word_to_linenumber, line_number=line_number)

    for complexword in complexword_set:
        if complexword in results:
            continue
        results.append(SpecificKeyword(
            headword=complexword, is_one_grame=True, line_numbers=word_to_linenumber[complexword]))

    return results


def _add_to_complexword_set(complexword_set: set, chunk, word_to_linenumber: DefaultDict[str, Deque], line_number):
    word = ''.join(chunk)
    word_to_linenumber[word].append(line_number)
    return complexword_set.add(word)


def _add_to_chunk(face, chunk):
    chunk.append(face)
