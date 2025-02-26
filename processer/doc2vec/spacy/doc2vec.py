from collections import deque
from pydoc import doc
from typing import Iterable
import spacy
from spacy.tokens import Doc
from data_loader.dto import DTO
from processer.data_loader import dto
from processer.doc2vec import sentiment
import multiprocessing


class Doc2Vec:

    def __init__(self, name, vectaizer, keyword_extracter, delimiter=".\n", **spacy_cofing):
        self.nlp = spacy.load(name=name, **spacy_cofing)
        self.delimiter = delimiter
        self.vectaizer = vectaizer
        self.keyword_extracter = keyword_extracter

    def exec(self, datas: Iterable[DTO]):
        ret = deque()
        for data in datas:
            doc = self._parse(dto=dto)

            vector, sentiment_results = self.vectaizer.exec(doc, data)
            keywords = self.keyword_extracter.exec(
                doc, vector, sentiment_results)
            ret.append((vector, sentiment_results, keywords, dto,))
        return ret

    def _parse(self, dto: DTO):
        text = self._get_text(dto)
        doc = self.nlp(text)
        return doc

    def _get_text(self, dto: DTO):
        return self.delimiter.join([dto.title, dto.body])


class Doc2VecChunkedBatch(Doc2Vec):
    def __init__(self, name, vectaizer, keyword_extracter, delimiter=".\n", batch_size=50, spacy_cofing={}):

        self.batch_size = batch_size
        super().__init__(name, vectaizer, keyword_extracter, delimiter, **spacy_cofing)

    def exec(self, datas_chunks: Iterable[Iterable[DTO]]):
        for datas_chunk in datas_chunks:
            id2data = {data.id: data for data in datas_chunk}
            texts = [(self._get_text(data), {
                      "text_id": data.id},) for data in datas_chunk]
            doc_tuples = self.nlp.pipe(
                texts=texts, batch_size=self.batch_size, n_process=multiprocessing.cpu_count)
            for doc, context in doc_tuples:
                dto = id2data[context["text_id"]]
                vector, sentiment_results = self.vectaizer.exec(doc, dto)

                keywords = self.keyword_extracter.exec(
                    doc, vector, sentiment_results)
                yield vector, sentiment_results, keywords, dto,
