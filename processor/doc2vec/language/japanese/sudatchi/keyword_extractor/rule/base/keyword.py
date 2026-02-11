
from collections import defaultdict, deque

from typing import DefaultDict, Deque, Dict, Iterable, List, Optional, Set


from data_loader.dto import DTO
from processor.doc2vec.base.protocol.postprocessor import DocVectorType, PostprocessorBase
from processor.doc2vec.base.protocol.keyword_extractor import ExtractResultDTO, KeywordExtractRule
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO

from sudachipy.morpheme import Morpheme
from doc2vec.util.specified_keyword import SpecifiedKeyword
from doc2vec.language.japanese.sudatchi.util import reguraize_rule
from doc2vec.language.japanese.sudatchi.util.matcher.preset import adjective_verb_possible, adverb_possible, counter_word, counter_word_possible, noun, number, prefix, safix, verb_noun_possible, verb
from doc2vec.language.japanese.sudatchi.util.matcher.preset import auxiliary_verb
from doc2vec.language.japanese.sudatchi.singleton import ModeA
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.base import stopwords


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


unuse_word_conditions = adverb_possible.matcher | adjective_verb_possible.matcher | number.matcher | counter_word.matcher | counter_word_possible.matcher | verb.matcher
noun_or_safix_matcher = noun.matcher | safix.matcher
whole_counter_word = counter_word.matcher | counter_word_possible.matcher

verb_next = auxiliary_verb.matcher | verb.matcher


class WordCanditates:
    canditates: Deque[Morpheme]
    word_to_tokens: DefaultDict[str, TokensDTO]
    start: Optional[int]
    end: int
    all_tokens: List[Morpheme]
    # all_text:str
    # def __init__(self, all_tokens: List[Morpheme], all_text):

    def __init__(self, all_tokens: List[Morpheme]):
        self.word_to_tokens = defaultdict(TokensDTO)
        self.all_tokens = all_tokens

        # self.all_text = all_text
        self.reset()

    def reset(self):
        self.canditates = deque()
        self.canditates_count = 0

        self.start = None
        self.int = -1

    def add_canditate(self, token: Morpheme, position):

        self.canditates.append(token)
        self.canditates_count += 1
        if self.start == None:
            self.start = position
        self.end = position

    def check(self):
        if self.canditates_count == 0:
            return
        canditates = self.canditates

        end = self.end
        self.reset()

        last_token = canditates[-1]

        if len(self.all_tokens) > end + 1:

            if verb_noun_possible.matcher(last_token):

                next_token = self.all_tokens[end + 1]
                if verb.matcher(next_token):
                    return
            elif adjective_verb_possible.matcher(last_token):
                next_token = self.all_tokens[end + 1]
                if verb_next(next_token):

                    return
            elif adverb_possible.matcher(last_token):
                next_token = self.all_tokens[end + 1]
                if verb_next(next_token):

                    return

        canditate_count = self.canditates_count

        if canditate_count == 1:
            token = canditates[0]
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
        canditates = self._count_check(canditates, canditate_count)
        if not canditates:
            return
        is_complexable_word = False
        count = 0
        for token in canditates:
            count += 1
            if not unuse_word_conditions(token) and not stopwords.matcher(token=token):
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

    def _count_check(self, canditates, canditate_count):
        head = canditates[0]

        if number.matcher(head):
            index = 0

            while index < canditate_count:

                token = canditates[index]
                index += 1

                if number.matcher(token) or whole_counter_word.matcher(token):
                    continue
                break
            if index == canditate_count:

                return False
            canditates = canditates[index - 1:]
        return canditates

    def get_word_to_token(self):

        return self.word_to_tokens


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, document_vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, postprocessor: PostprocessorBase):

        word_canditate = WordCanditates(all_tokens=parse_result.tokens)

        position = -1
        for token in parse_result.tokens:
            position += 1

            if noun_or_safix_matcher(token) or prefix.matcher(token):
                word_canditate.add_canditate(token, position=position)
                continue
            word_canditate.check()
        word_canditate.check()
        for headword, token_dto in word_canditate.get_word_to_token().items():

            sk = SpecifiedKeyword(
                headword=headword, tokens=token_dto.tokens, is_force=token_dto.is_force)
            results.add_keyword(sk)
        return results
