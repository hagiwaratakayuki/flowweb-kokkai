from collections import deque
from data_loader.dto import DTO
from doc2vec.base.protocol.indexer import IndexerCls
from doc2vec.base.protocol.tokenizer import TokenizerCls

from .vectorizer.gensim import MODEL_PATH, Vectorizer


from multiprocessing.pool import Pool
from typing import Iterable


class Doc2Vec:
    def __init__(self, indexer: IndexerCls, tokenaizer: TokenizerCls, chunksize=1000) -> None:
        self._tokenaizer = tokenaizer
        self._indexer = indexer

        self._chunk_size = chunksize

    def exec(self, pool: Pool, datas: Iterable[DTO]):
        dto_map = {}
        generater = self.get_data_itr(dtos=datas, data_map=dto_map)

        for parse_result, data_id in pool.imap(func=self._tokenaizer.parse, iterable=generater, chunksize=self._chunk_size):
            dto = dto_map[data_id]
            yield self._indexer.exec(parse_result, dto)

    def get_data_itr(self, dtos: Iterable[DTO], data_map):

        for dto in dtos:
            data_map[dto.id] = dto

            yield dto.get_text(), dto.id
