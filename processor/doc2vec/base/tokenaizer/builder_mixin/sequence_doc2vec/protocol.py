from abc import ABCMeta, abstractmethod

from doc2vec.base.facade.sequence_doc2vec.builder.root import SequenceDoc2VecBuilderRoot


class TokenaizerSequenceDoc2VecBuilderMixin(SequenceDoc2VecBuilderRoot, metaclass=ABCMeta):
    pass
