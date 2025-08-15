
from collections import defaultdict, deque

from typing import DefaultDict, Deque, Dict, Iterable, Set

from numpy import iterable
from data_loader.dto import DTO
from doc2vec.base.protocol.indexer import DocVectorType, IndexerCls
from doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from sudachipy import tokenizer
from sudachipy.morpheme import Morpheme
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.language.japanese.sudatchi.util import reguraize_rule
from doc2vec.language.japanese.sudatchi.util.matcher.preset import adjective_verb_possible, adverb_possible, counter_word, counter_word_possible, noun, number, prefix, safix, verb_noun_possible
ModeA = tokenizer.Tokenizer.SplitMode.A


class TokensDTO:
    def __init__(self):
        self.tokens = set()
        self.is_force = False
        self.subwords = []
        self.headword = ''

    def set_headword(self, headword):
        self.headword = headword

    def add_subwords(self, subword):
        self.subwords.append(subword)

    def update(self, tokens: Iterable, is_force=False):
        self.tokens.update(tokens)
        self.is_force = is_force

    def add(self, token, is_force=False):
        self.tokens.add(token)
        self.is_force = self.is_force or is_force


unuse_word_conditions = adverb_possible.matcher | adjective_verb_possible.matcher | number.matcher | counter_word.matcher | counter_word_possible.matcher
noun_or_safix_matcher = noun.matcher | safix.matcher
whole_counter_word = counter_word.matcher | counter_word_possible.matcher


class WordCanditates:
    canditates: Deque[Morpheme]
    word_to_tokens: DefaultDict[str, TokensDTO]

    def __init__(self):
        self.canditates = deque()

        self.canditates_count = 0
        self.word_to_tokens = defaultdict(TokensDTO)

    def add_canditate(self, token: Morpheme):
        self.canditates.append(token)
        self.canditates_count += 1

    def check(self):

        canditates = self.canditates
        self.canditates = deque()
        canditate_count = self.canditates_count
        self.canditates_count = 0
        if canditate_count == 0:
            return
        if canditate_count == 1:
            token = canditates.pop()
            if unuse_word_conditions(token):
                return
            if verb_noun_possible.matcher(token):
                self.word_to_tokens[reguraize_rule.apply(token)].add(
                    token=token, is_force=True)
                return
            splited = token.split(ModeA)
            if len(splited) > 1:
                tail = splited[-1]
                if verb_noun_possible.matcher(tail):
                    head = ''.join([reguraize_rule.apply(t)
                                   for t in splited if t != tail])
                    self.word_to_tokens[head].add(token=token)
                    self.word_to_tokens[reguraize_rule.apply(
                        splited[-1])].add(token, is_force=True)
                    return

        is_complexable_word = False
        count = 0
        for token in canditates:
            count += 1
            if not unuse_word_conditions(token):
                is_complexable_word = True
                break
        if not is_complexable_word:
            return
        tail = canditates.pop()
        if count == canditate_count and safix.matcher(tail):
            return
        is_counter_tail = counter_word.matcher(tail)

        second_tail = None
        if not is_counter_tail and counter_word_possible.matcher(tail):
            second_tail = canditates.pop()
            is_counter_tail = number.matcher(second_tail)
            if not is_counter_tail:
                canditates.append(second_tail)
        canditates.append(tail)
        word = ''
        subword = ''
        if not is_counter_tail:

            word = ''.join([reguraize_rule.apply(t)
                            for t in canditates])
        else:

            sliced_canditates = deque()
            is_sub_mode = False

            for token in canditates:

                if token.surface()[-1] == '法':
                    word += reguraize_rule.apply(token)
                    sliced_canditates.append(token)
                    canditates = sliced_canditates

                    break
                if is_counter_tail and number.matcher(token):

                    canditates = sliced_canditates
                    break

                word += reguraize_rule.apply(token)

        self.word_to_tokens[word].update(canditates)

    def get_word_to_token(self):
        self.check()
        return self.word_to_tokens


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, document_vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, indexer: IndexerCls):
        tokens: DefaultDict[str, TokensDTO] = defaultdict(TokensDTO)
        word_canditate = WordCanditates()
        for token in parse_result.tokens:
            if noun_or_safix_matcher(token) or (word_canditate.canditates_count > 0 and prefix.matcher(token)):
                word_canditate.add_canditate(token)
                continue
            word_canditate.check()

        for headword, token_dto in word_canditate.get_word_to_token().items():
            sk = SpecifiedKeyword(
                headword=headword, source_ids=token_dto.tokens, is_force=token_dto.is_force)
            results.add_keyword(sk)
        return results
