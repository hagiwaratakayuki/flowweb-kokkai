

from typing import Type
from .root import SequenceDoc2VecBuilderRoot
from doc2vec.base.facade.sequence_doc2vec.facade_class import Doc2Vec


class SequenceDoc2VecBuilder(SequenceDoc2VecBuilderRoot):
    facade_class: Type[Doc2Vec] = Doc2Vec

    def __init__(self):
        self.tokenaier_params = {}
        self.document_vectoraier_params = {}
        self.keyword_extractor_params = {}

    def build(self, chunksize=1000, kwargs={}):
        return self.facade_class(document_vectoraizer=self._build_document_vectoraizer(),
                                 tokenaizer=self._build_tokenaizer(),
                                 keyword_extractor=self._build_keyword_extractor(),
                                 chunksize=chunksize, **kwargs)

    def _build_keyword_extractor(self):
        return self.keyword_extractor_class(**self.keyword_extractor_class)

    def _build_tokenaizer(self):
        return self.tokenaier_class(**self.tokenaier_params)

    def _build_document_vectoraizer(self):
        return self.document_vectoraizer_class(**self.document_vectoraier_params)
