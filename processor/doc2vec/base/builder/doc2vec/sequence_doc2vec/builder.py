
from doc2vec.base.builder.components.mixins.use_filter import UseFilterMixin
from doc2vec.base.builder.doc2vec.sequence_doc2vec.root import SequenceDoc2VecBuilderRoot


class SequenceDoc2VecBuilder(UseFilterMixin, SequenceDoc2VecBuilderRoot):
    def _build_keyword_extractor(self):
        pass

    def _build_tokenaizer(self):
        params = self._call_filters()

    def _build_document_vectoraizer(self):
        pass
