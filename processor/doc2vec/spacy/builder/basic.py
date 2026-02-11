import keyword
from multiprocessing import cpu_count
from typing import Callable, Type

from processor.doc2vec.base.keyword_extractor.basic import BasicKeywordExtractor


class SpacyBasicBuilder:
    keyword_extractor: Type[BasicKeywordExtractor] = B
    projector: Callable

    def build(self, name, keyword_extractor: BasicKeywordExtractor, sentiment: BasicSentiment, vectoraizer: Optional[BasicVectoraizer] = None, projecter=project_vector, batch_size=None, n_process=-1, delimiter=".\n", spacy_cofing={}):
        self.nlp = spacy.load(name=name, **spacy_cofing)
        self.delimiter = delimiter
        self.vectoraizer = vectoraizer or BasicVectoraizer()

        sentiment.initialize(nlp=self.nlp, projecter=projecter)
        self.vectoraizer.initialize(sentiment=sentiment, projecter=projecter)
        self.keyword_extractor = keyword_extractor

        self.batch_size = batch_size or 1000
        self.n_process = n_process or cpu_count()

    def _build_postprocessor(self):
        pass

    def _build_keyword_extractor(self):
        pass
