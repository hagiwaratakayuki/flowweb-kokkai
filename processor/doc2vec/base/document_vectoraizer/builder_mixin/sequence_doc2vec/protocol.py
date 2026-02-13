from abc import ABCMeta, abstractmethod
from processor.doc2vec.base.facade.sequence_doc2vec.builder.root import SequenceDoc2VecBuilderRoot


class DocumentVectoraizerSequenceDoc2VecMixin(SequenceDoc2VecBuilderRoot, metaclass=ABCMeta):
    @abstractmethod
    def use_document_vectoraier(self, *args, **kwargs):
        pass
