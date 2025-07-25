
from data_loader.dto import DTO
from doc2vec.base.protocol.indexer import DocVectorType, IndexerCls
from doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from sudachipy import tokenizer

from doc2vec.util.specified_keyword import SpecifiedKeyword
ModeA = tokenizer.Tokenizer.SplitMode.A


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, indexer: IndexerCls):
        checked = set()
        for token in parse_result.tokens:
            if token.normalized_form() in checked:
                continue
            part_of_speech = token.part_of_speech()
            if part_of_speech[0] != '名詞' or part_of_speech[1] == '数詞' or part_of_speech[2] == '助数詞':
                continue
            if part_of_speech[2] == 'サ変可能':
                SpecifiedKeyword(headword=)
            splited = token.split(ModeA)
            if splited[-1].part_of_speech()[2] == 'サ変可能':
                head = []
