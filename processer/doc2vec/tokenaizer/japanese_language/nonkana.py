

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
    chunk = ''
    concat_count = False

    for line, tokens in parse_results:
        if len(chunk) > 1:
            nonhiragana_set.add(chunk)
        chunk = ''
        for face, data in tokens:
            chunklen = len(chunk)

            if data[0] == '接頭詞':
                chunk = ''
                continue
            if data[2] == '数助詞':
                if chunklen > 0:
                    chunk += face
                else:
                    chunk = ''
                    continue

            if eisuu.search(face) is not None:
                chunk += face
                continue
            if kigou.search(face) is not None:
                if chunklen > 0:

                    if data[1] == '括弧開' or data[1] == '括弧閉' or data[1] == 'サ変接続' or data[1] == '句点' or data[1] == '読点':
                        nonhiragana_set.add(chunk)
                        chunk = ''

                    else:
                        chunk += face
                continue
            if data[1] == 'サ変接続':
                if chunklen > 0:
                    chunk += face
                else:
                    chunk = ''
                continue
            if data[1] == '接尾':
                if chunklen > 1:
                    chunk += face
                    nonhiragana_set.add(chunk)
                chunk = ''
                continue
            if data[1] == '名詞':
                chunk += face
                continue

            if chunklen > 1:
                nonhiragana_set.add(chunk)
            chunk = ''

    for nonhiragana in check_stopword_with_itr(nonhiragana_set):
        if nonhiragana in results:
            continue
        results.append(SpecificKeyword(
            headword=nonhiragana, is_one_grame=True))

    return results
