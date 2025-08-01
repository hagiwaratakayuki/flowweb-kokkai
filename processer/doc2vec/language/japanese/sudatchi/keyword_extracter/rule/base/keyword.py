
from collections import defaultdict, deque

from typing import DefaultDict, Deque, Iterable
from data_loader.dto import DTO
from doc2vec.base.protocol.indexer import DocVectorType, IndexerCls
from doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from sudachipy import tokenizer
from sudachipy.morpheme import Morpheme
from doc2vec.util.specified_keyword import SpecifiedKeyword
from processer.doc2vec.language.japanese.sudatchi.util import reguraize_rule
ModeA = tokenizer.Tokenizer.SplitMode.A


class TokensDTO:
    def __init__(self):
        self.tokens = set()
        self.is_force = False

    def add(self, token, is_force=False):
        self.tokens.add(token)
        self.is_force = self.is_force or is_force


数詞と助数詞 = {'数詞', '助数詞可能'}


class Pending:
    pendings: Deque[Morpheme]

    def __init__(self):
        self.pendings = deque()
        self.is_pending = False

    def add_pending(self, token: Morpheme):
        self.pendings.append(token)
        self.is_pending = True

    def release(self):
        self.is_pending = False
        pendings = self.pendings
        self.pendings = deque()
        if not self.is_pending:
            return False, None, None
        is_complexable_word = False
        for token in pendings:
            part_of_speech = token.part_of_speech()
            if part_of_speech[1] != '数詞' and '助数詞' not in part_of_speech[2] and part_of_speech[2] != '副詞可能' and part_of_speech[2] != '副詞可能':
                is_complexable_word = True
                break


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, indexer: IndexerCls):
        tokens: DefaultDict[str, TokensDTO] = defaultdict(TokensDTO)
        is_pending = False
        pending_tokens = deque()
        for token in parse_result.tokens:

            part_of_speech = token.part_of_speech()
            if part_of_speech[1] == '数詞':
                is_pending = True
                pending_tokens.append()
            if part_of_speech[0] != '名詞' or part_of_speech[2] == '助数詞':
                if is_pending:
                    is_pending
                continue
            if part_of_speech[2] == 'サ変可能':
                tokens[reguraize_rule.apply(token)].add(
                    token=token, is_force=True)
                continue

            splited = token.split(ModeA)
            if len(splited) > 1:
                if splited[-1].part_of_speech()[2] == 'サ変可能':
                    head = ''.join([reguraize_rule.apply(t)
                                   for t in splited[:-1]])
                    tokens[head].add(token=token)
                    tokens[reguraize_rule.apply(
                        splited[-1])].add(token, is_force=True)
                    continue
            tokens[reguraize_rule.apply(token)].add(token=token)
        for headword, token_dto in tokens.items():
            sk = SpecifiedKeyword(
                headword=headword, source_ids=token_dto.tokens, is_force=token_dto.is_force)
            results.add_keyword(sk)
        return results
