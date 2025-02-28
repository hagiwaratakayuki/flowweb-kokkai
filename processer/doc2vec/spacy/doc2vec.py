from collections import deque
from pydoc import doc
from typing import Dict, Iterable, List, Optional
import spacy
from spacy.tokens import Doc
from data_loader.dto import DTO
import multiprocessing

from doc2vec.spacy.vectaizer.cls import BasicVectaizer
from doc2vec.spacy.keyword_extracter.cls import BasicKeywordExtratcer
from processer.doc2vec.spacy.vectaizer.sentiment import BasicSentiment


class SpacyDoc2Vec:

    def __init__(self, name, keyword_extracter: BasicKeywordExtratcer, sentiment: BasicSentiment, vectaizer: Optional[BasicVectaizer] = None, delimiter=".\n", batch_size=50, spacy_cofing={}):
        self.nlp = spacy.load(name=name, **spacy_cofing)
        self.delimiter = delimiter
        self.vectaizer = vectaizer or BasicVectaizer()
        self.keyword_extracter = keyword_extracter
        self.batch_size = batch_size

    def exec(self, datas: Iterable[DTO]):
        ret = deque()
        id2data = {}
        texts = self._get_itr(datas=datas, id2data=id2data)
        doc_tuples = self.nlp.pipe(
            texts=texts, batch_size=self.batch_size, n_process=multiprocessing.cpu_count)
        for data in datas:

            vector, sentiment_results = self.vectaizer.exec(doc, data)
            keywords = self.keyword_extracter.exec(
                doc, vector, sentiment_results)
            for doc, context in doc_tuples:
                dto = id2data[context["text_id"]]
                vector, sentiment_results = self.vectaizer.exec(doc, dto)

                keywords = self.keyword_extracter.exec(
                    doc, vector, sentiment_results, dto)
                ret.append((vector, sentiment_results, keywords, dto,))

        return ret

    def _get_itr(self, datas: List[DTO], id2data: Dict):
        for data in datas:
            id2data[data.id] = data
            yield self._get_text(data), {"text_id": data.id}

    def _parse(self, dto: DTO):
        text = self._get_text(dto)
        doc = self.nlp(text)
        return doc

    def _get_text(self, dto: DTO):
        return self.delimiter.join([dto.title, dto.body])
