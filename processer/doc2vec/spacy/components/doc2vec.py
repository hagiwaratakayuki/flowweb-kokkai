from collections import deque
from typing import Dict, Iterable, List, Optional
import spacy
from spacy.tokens import Doc
from data_loader.dto import DTO


from doc2vec.spacy.components.vectoraizer.cls import BasicVectoraizer
from doc2vec.spacy.components.keyword_extracter.cls import BasicKeywordExtratcer
from doc2vec.spacy.components.sentiment.cls import BasicSentiment
from doc2vec.spacy.components.commons.projections import project_vector


class SpacyDoc2Vec:

    def __init__(self, name, keyword_extracter: BasicKeywordExtratcer, sentiment: BasicSentiment, vectoraizer: Optional[BasicVectoraizer] = None, projecter=project_vector, batch_size=None, n_process=-1, delimiter=".\n", spacy_cofing={}):
        self.nlp = spacy.load(name=name, **spacy_cofing)
        self.delimiter = delimiter
        self.vectoraizer = vectoraizer or BasicVectoraizer()

        sentiment.initialize(nlp=self.nlp, projecter=projecter)
        self.vectoraizer.initialize(sentiment=sentiment, projecter=projecter)
        self.keyword_extracter = keyword_extracter
        self.keyword_extracter.initialize(projeccter=projecter)
        self.batch_size = batch_size
        self.n_process = n_process

    def exec(self, datas: Iterable[DTO]):
        ret = deque()
        id2data = {}
        iter = self._get_itr(datas=datas, id2data=id2data)
        doc_tuples = self.nlp.pipe(
            iter, n_process=self.n_process, batch_size=self.batch_size, as_tuples=True)

        for doc, context in doc_tuples:
            data = id2data[context["text_id"]]
            vector, sentiment_results = self.vectoraizer.exec(doc, data)

            keywords = self.keyword_extracter.exec(
                doc, vector, sentiment_results, data)
            ret.append((vector, sentiment_results, keywords, data,))

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
        res = ''
        if dto.title:
            res += dto.title + self.delimiter
        res += dto.body
        return res
