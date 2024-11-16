

from operator import is_not
from typing import List
from doc2vec.util.specific_keyword import SpecificKeyword
import regex as re

from .extract_stopwords import check_stopword, check_stopword_with_itr


eisuu = re.compile(r'^[\w\d]+$', re.A)
kigou = re.compile(r'^\W+$')
kuuhaku = re.compile(r'\s+')
hiragana_pt = re.compile(r'[\p{Hiragana},。、]')


def extract(results: List[SpecificKeyword], parse_results: List, data):
    nonhiragana_set = set()
    chunk = []
    chunklen = 0

    for line, tokens in parse_results:
        if chunklen > 1:
            _add_to_nonhiragana_set(
                nonhiragana_set=nonhiragana_set, chunk=chunk)
        chunk = []
        chunklen = 0
        for face, data in tokens:
            chunklen = len(chunk)

            if data[0] == '接頭詞':
                chunk = []
                continue
            if data[2] == '数助詞':
                if chunklen > 0:
                    _add_to_chunk(face, chunk)
                else:
                    chunk = []
                    continue

            if eisuu.search(face) is not None:
                _add_to_chunk(face, chunk)
                continue
            if kigou.search(face) is not None:
                if chunklen > 1:

                    if data[1] == '括弧開' or data[1] == '括弧閉' or data[1] == 'サ変接続' or data[1] == '句点' or data[1] == '読点':
                        _add_to_nonhiragana_set(
                            nonhiragana_set=nonhiragana_set, chunk=chunk)
                        chunk = []

                    else:
                        _add_to_chunk(face=face, chunk=chunk)
                continue

            if data[1] == '接尾':
                if chunklen > 0:
                    _add_to_chunk(face=face, chunk=chunk)
                    _add_to_nonhiragana_set(nonhiragana_set, chunk)
                chunk = []

                continue
            if data[1] == '名詞':
                _add_to_chunk(face, chunk)
                continue

            if chunklen > 1:
                _add_to_nonhiragana_set(nonhiragana_set=nonhiragana_set)
            chunk = []
    chunklen = len(chunk)
    if chunklen > 1:
        _add_to_nonhiragana_set(nonhiragana_set=nonhiragana_set, chunk=chunk)
    for nonhiragana in check_stopword_with_itr(nonhiragana_set):
        if nonhiragana in results:
            continue
        results.append(SpecificKeyword(
            headword=nonhiragana, is_one_grame=True))

    return results


def _add_to_nonhiragana_set(nonhiragana_set: set, chunk):
    return nonhiragana_set.add(''.join(chunk))


def _add_to_chunk(face, chunk):
    chunk.append(face)
