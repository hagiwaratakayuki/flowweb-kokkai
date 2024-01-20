from typing import Iterable
from doc2vec.indexer.cls import Indexer
from doc2vec.tokenaizer.nltk_tokenaizer import NLTKTokenazer
from multiprocessing.pool import Pool

from doc2vec.vectaizer.gensim_fasttext import Vectaizer, MODEL_PATH
from doc2vec.sentiment.nltk_analizer import NLTKAnalizer
from collections import deque

from data_loader.dto import DTO


class Doc2Vec:
    def __init__(self, modelfile: str = MODEL_PATH, workers: int = 1) -> None:
        tokenaizer = NLTKTokenazer()
        vectaizer = Vectaizer(modelfile)
        analizer = NLTKAnalizer()
        self._workers = workers
        self._vectaizer = vectaizer
        self._indexer = Indexer(tokenaizer=tokenaizer,
                                sentimentAnalyzer=analizer)

    def exec(self, pool: Pool,  datas: Iterable[DTO]):
        data_dict = {}
        generater = self.get_data_itr(datas=datas, data_dict=data_dict)

        parsed = pool.imap_unordered(
            func=self._indexer.parse, iterable=generater)

        with_word_vector = self.get_word_vector(parsed)

        compupteds = pool.imap_unordered(
            func=self._indexer.compute, iterable=with_word_vector, chunksize=1000)
        for vector, sentimentResults, scored_keywords, dataid in compupteds:
            yield vector, sentimentResults, scored_keywords, data_dict[dataid]

    def get_data_itr(self, datas: Iterable[DTO], data_dict: dict):
        counted_id = 0
        for data in datas:
            data_dict[counted_id] = data
            yield (data.title + '\n' + data.body, counted_id, )
            counted_id += 1

    def get_word_vector(self, parse_itr):
        for first, keywords, third in parse_itr:

            yield first, self._vectaizer.exec_dict(keywords), third
