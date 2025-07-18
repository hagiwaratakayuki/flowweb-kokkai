from collections import deque
from data_loader.dto import DTO
from processer.doc2vec.base.protocol.indexer import IndexerCls
from processer.doc2vec.base.protocol.tokenizer import TokenizerCls

from .vectaizer.gensim import MODEL_PATH, Vectaizer


from multiprocessing.pool import Pool
from typing import Iterable


class Doc2Vec:
    def __init__(self, indexer: IndexerCls, tokenaizer: TokenizerCls, is_use_title=True, line_break=r'\n', chunksize=1000) -> None:
        self._tokenaizer = tokenaizer
        self._indexer = indexer
        self._is_use_title = is_use_title
        self._line_break = line_break

        self._chunk_size = chunksize

    def exec(self, pool: Pool, datas: Iterable[DTO]):
        dto_map = {}
        generater = self.get_data_itr(dtos=datas, data_map=dto_map)

        for parse_result, data_id in pool.imap_unordered(func=self._tokenaizer.parse, iterable=generater, chunksize=self._chunk_size):
            dto = dto_map[data_id]
            yield self._indexer.exec(parse_result, dto)

    def get_data_itr(self, dtos: Iterable[DTO], data_map):

        for dto in dtos:
            data_map[dto.id] = dto
            if self._is_use_title:
                text = dto.title + self._line_break + dto.body
            else:
                text = dto.body
            yield text, dto.id

    def get_word_vector(self, parse_itr, dto_map):

        for first, tokens, keywords, third, force in parse_itr:

            vector, sentimentResults, scored_keywords, dataid = self._indexer.compute(
                [first, self._vectaizer.exec_dict(tokens), keywords, third, force])

            yield vector, sentimentResults, scored_keywords, dto_map[dataid]
