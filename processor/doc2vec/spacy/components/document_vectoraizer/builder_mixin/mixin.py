from typing import Type
from doc2vec.base.document_vectoraizer.builder_mixin.sequence_doc2vec.protocol import DocumentVectoraizerSequenceDoc2VecMixin
from doc2vec.spacy.components.document_vectoraizer.cls import SpacyBasicDocumentVectoraizer


class SpacyDocumentVectoraizerBuilderMixin(DocumentVectoraizerSequenceDoc2VecMixin):
    document_vectoraizer_class: Type[SpacyBasicDocumentVectoraizer] = SpacyBasicDocumentVectoraizer

    def use_document_vectoraier(self, kwargs={}):

        self.document_vectoraier_params.update(kwargs)
        return self
