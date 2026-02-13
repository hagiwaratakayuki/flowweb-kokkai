from processor.doc2vec.base.facade.sequence_doc2vec.builder.basic_implement import SequenceDoc2VecBuilder
from processor.doc2vec.spacy.components.document_vectoraizer.builder_mixin.mixin import SpacyDocumentVectoraizerBuilderMixin
from processor.doc2vec.spacy.components.keyword_extractor.builder_plugin.sequence_doc2vec import SpacyKeywordExtractorSequenceDoc2VecBuilderMixin
from processor.doc2vec.spacy.components.sentiment.builder_mixin import SpacySentimentBuilderMixin


class SpacySequenceDoc2VecBuilder(
    SequenceDoc2VecBuilder,
    SpacyDocumentVectoraizerBuilderMixin,
    SpacySentimentBuilderMixin,
    SpacyKeywordExtractorSequenceDoc2VecBuilderMixin
):
    pass
