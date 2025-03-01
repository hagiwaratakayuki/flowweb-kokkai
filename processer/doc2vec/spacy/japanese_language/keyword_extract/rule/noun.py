from collections import defaultdict

from typing import Dict, List, Set

from ..stopwords import remove_stopwords
from ..util.inflection_check import is_sahen, is_adverbable, is_tail
from doc2vec.spacy.keyword_extracter.protocol import KeywordExtractRule, TokenID2Keyword
from spacy.tokens import Doc

from doc2vec.util.specified_keyword import SpecifiedKeyword


class NounDTO:
    faces: Set[str]
    source_ids: Set[int]
    is_force: bool
    vector: any

    def __init__(self):
        self.faces = set()
        self.source_ids = set()
        self.is_force = False


IGNORE_TAG = {'compound', 'nmod', 'obl'}
MAIN_TAG = {'nsubj', 'ROOT'}


class NounExtractRule(KeywordExtractRule):
    def execute(self, doc: Doc, vector, sentiment_results, dto, results: List, tokenid2keyword: TokenID2Keyword):

        noun_datas = defaultdict(NounDTO)

        for sent in doc.sents:

            for token in sent:
                if token.pos_ == "NOUN" and is_sahen.check(token) == False and is_adverbable.check(token) == False and is_tail.check(token) == False and token.tag_ not in IGNORE_TAG:
                    if token.i > 0:
                        if doc[token.i - 1].tag_ in IGNORE_TAG:
                            continue

                    noun_data = noun_datas[token.norm_]
                    noun_data.faces.add(token.orth_)
                    noun_data.source_ids.add(token.i)
                    noun_data.is_force |= token.tag_ in MAIN_TAG
                    noun_data.vector = vector
        noun_datas = {noun: noun_datas[noun]
                      for noun in remove_stopwords(noun_datas.keys())}

        sks = [SpecifiedKeyword(
            headword=noun, vector=data.vector, target_words=data.faces, is_force=data.is_force, source_ids=data.source_ids) for noun, data in noun_datas.items()]
        for sk in sks:
            for sourceid in sk.source_ids:
                tokenid2keyword[sourceid][sk.id] = sk
        return sks, tokenid2keyword
