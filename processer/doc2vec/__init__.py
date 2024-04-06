from typing import Iterable
from doc2vec.indexer.cls import Indexer
from doc2vec.tokenaizer.nltk_tokenaizer import NLTKTokenazer
from multiprocessing.pool import Pool

from doc2vec.vectaizer.gensim_fasttext import Vectaizer, MODEL_PATH
from doc2vec.sentiment.nltk_analizer import NLTKAnalizer


from data_loader.dto import DTO


class Doc2Vec:
    def __init__(self, is_use_title=True, modelfile: str = MODEL_PATH, chunksize=1000, TokenaizerClass=NLTKTokenazer, VectaizerClass=Vectaizer, AnalizerClass=NLTKAnalizer, IndexerClass=Indexer) -> None:
        tokenaizer = TokenaizerClass()
        vectaizer = VectaizerClass(modelfile)
        analizer = AnalizerClass()
        self._chunk_size = chunksize
        self._is_use_title = is_use_title

        self._vectaizer = vectaizer
        self._indexer = IndexerClass(tokenaizer=tokenaizer,
                                     sentimentAnalyzer=analizer,
                                     is_use_title=is_use_title
                                     )

    def exec(self, pool: Pool,  datas: Iterable[DTO]):
        dto_map = {}
        generater = self.get_data_itr(dtos=datas, data_map=dto_map)

        parsed = pool.imap_unordered(
            func=self._indexer.parse, iterable=generater, chunksize=self._chunk_size)
        return self.get_word_vector(parsed, dto_map=dto_map)

        """
        with_word_vector = self.get_word_vector(parsed)
        
        compupteds = pool.imap_unordered(
            func=self._indexer.compute, iterable=with_word_vector, chunksize=self._chunk_size)

        for vector, sentimentResults, scored_keywords,  dataid in compupteds:

            yield vector, sentimentResults, scored_keywords, data_dict[dataid]
        """

    def get_data_itr(self, dtos: Iterable[DTO], data_map):

        for dto in dtos:
            data_map[dto.id] = dto
            yield dto

    def get_word_vector(self, parse_itr, dto_map):

        for first, keywords, third, force in parse_itr:

            vector, sentimentResults, scored_keywords,  dataid = self._indexer.compute(
                [first, self._vectaizer.exec_dict(keywords), third, force])
            yield vector, sentimentResults, scored_keywords,  dto_map[dataid]
