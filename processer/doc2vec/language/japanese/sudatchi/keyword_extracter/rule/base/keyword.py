import token
from typing import Dict
from processer.data_loader.dto import DTO
from processer.doc2vec.base.protocol.indexer import DocVectorType, IndexerCls
from processer.doc2vec.base.protocol.keyword_extracter import ExtractResultDTO, KeywordExtractRule
from processer.doc2vec.base.protocol.sentiment import SentimentResult
from processer.doc2vec.language.japanese.sudatchi.tokenaizer import SudatchiDTO


class Rule(KeywordExtractRule):
    def execute(self, parse_result: SudatchiDTO, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, indexer: IndexerCls):
        checked = set()
        for token in parse_result.tokens:
            if token.normalized_form() in checked:
                continue
            if token.
