from collections import deque
from data_loader.dto import DTO
from doc2vec.base.protocol.document_vectoraizor import AbstractDocumentVectoraizer
from doc2vec.base.protocol.keyword_extractor import AbstractKeywordExtractor
from doc2vec.base.protocol.tokenizer import AbstarctTokenizerClass


from multiprocessing.pool import Pool
from typing import Iterable

from processor.doc2vec.base.protocol.pipeline_keyord_extractor import AbstractPipelineKeywordExtractor


class Doc2Vec:
    def __init__(self, tokenaizer: AbstarctTokenizerClass, document_vectoraizer: AbstractDocumentVectoraizer, keyword_extractor: AbstractPipelineKeywordExtractor, chunksize=1000) -> None:
        self._tokenaizer = tokenaizer
        self._document_vectoraizer = document_vectoraizer
        self._keyword_extractor = keyword_extractor

        self._chunk_size = chunksize

    def exec(self, pool: Pool, datas: Iterable[DTO]):
        dto_map = {}
        generater = self.get_data_itr(dtos=datas, data_map=dto_map)
        ret = deque()

        for parse_result, data_id in pool.imap(func=self._tokenaizer.parse, iterable=generater, chunksize=self._chunk_size):
            dto = dto_map[data_id]
            vector, sentiment_results, token_2_score = self._document_vectoraizer.exec(
                parse_result, dto)

            keywords = self._keyword_extractor.exec(
                parse_result=parse_result, vector=vector, sentiment_results=sentiment_results, dto=dto, token_2_score=token_2_score)
            ret.append((vector, sentiment_results, keywords, dto,))
        return ret

    def get_data_itr(self, dtos: Iterable[DTO], data_map):

        for dto in dtos:
            data_map[dto.id] = dto

            yield dto.get_text(), dto.id
