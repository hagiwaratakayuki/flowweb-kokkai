from collections import deque
from multiprocessing import cpu_count
from typing import Dict, Iterable, List, Optional
from unittest import result
import spacy
from spacy.tokens import Doc
from data_loader.dto import DTO


from doc2vec.spacy.components.postprocessor.cls import BasicPostprocessor
from doc2vec.spacy.components.keyword_extractor.cls import BasicKeywordExtratcer
from doc2vec.spacy.components.sentiment.cls import BasicSentiment
from doc2vec.spacy.components.commons.projections import project_vector


class SpacyDoc2Vec:

    def __init__(self, name, keyword_extractor: BasicKeywordExtratcer, sentiment: BasicSentiment, vectoraizer: Optional[BasicPostprocessor] = None, projecter=project_vector, batch_size=None, n_process=-1, delimiter=".\n", spacy_cofing={}):
        self.nlp = spacy.load(name=name, **spacy_cofing)
        self.delimiter = delimiter
        self.vectoraizer = vectoraizer or BasicPostprocessor()

        sentiment.initialize(nlp=self.nlp, projecter=projecter)
        self.vectoraizer.initialize(
            sentiment_analaizer=sentiment, projecter=projecter)
        self.keyword_extractor = keyword_extractor

        self.batch_size = batch_size or 1000
        self.n_process = n_process or cpu_count()

    def exec(self, datas: Iterable[DTO]):

        ret = deque()
        id2data = {}
        iter = self._get_itr(datas=datas, id2data=id2data)

        doc_tuples = list(self.nlp.pipe(
            iter, n_process=self.n_process, batch_size=self.batch_size, as_tuples=True))

        for doc, context in doc_tuples:
            data = id2data[context["text_id"]]

            vector, sentiment_results, token_2_score = self.vectoraizer.exec(
                doc, data)

            keywords = self.keyword_extractor.exec(
                parse_result=doc, vector=vector, sentiment_results=sentiment_results, dto=data, token_2_score=token_2_score)
            ret.append((vector, sentiment_results, keywords, data,))

        return ret

    def _get_itr(self, datas: List[DTO], id2data: Dict):
        result = deque()
        try:
            for data in datas:
                id2data[data.id] = data
                result.append((self._get_text(data), {"text_id": data.id}, ))
        except RuntimeError:
            pass
        return result

    def _get_text(self, dto: DTO):
        res = ''
        if dto.title:
            res += dto.title + self.delimiter
        res += dto.body
        return res
