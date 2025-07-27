
from collections import defaultdict
from operator import is_
from typing import DefaultDict
from data_loader.dto import DTO
from doc2vec.base.protocol.indexer import DocVectorType, IndexerCls
from doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from sudachipy import tokenizer

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


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, indexer: IndexerCls):
        tokens: DefaultDict[str, TokensDTO] = defaultdict(TokensDTO)
        for token in parse_result.tokens:

            part_of_speech = token.part_of_speech()
            if part_of_speech[0] != '名詞' or part_of_speech[1] == '数詞' or part_of_speech[2] == '助数詞':
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
