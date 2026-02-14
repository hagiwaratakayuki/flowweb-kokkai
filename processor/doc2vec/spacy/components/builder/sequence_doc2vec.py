from doc2vec.base.facade.sequence_doc2vec.builder.basic_implement import SequenceDoc2VecBuilder
from doc2vec.spacy.components.document_vectoraizer.builder_mixin.mixin import SpacyDocumentVectoraizerBuilderMixin
from doc2vec.spacy.components.keyword_extractor.builder_plugin.sequence_doc2vec import SpacyKeywordExtractorSequenceDoc2VecBuilderMixin
from doc2vec.spacy.components.sentiment.builder_mixin import SpacySentimentBuilderMixin
from doc2vec.spacy.components.tokenaizer.builder_mixin.sequence_doc2vec import SpacyTokenizerSequenceDoc2VecBuilderMixin
from doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.mixin import SpacyNLPSequenceDoc2VecBuilderMixin


class SpacySequenceDoc2VecBuilder(
    SequenceDoc2VecBuilder,
    SpacyDocumentVectoraizerBuilderMixin,
    SpacySentimentBuilderMixin,
    SpacyKeywordExtractorSequenceDoc2VecBuilderMixin,
    SpacyTokenizerSequenceDoc2VecBuilderMixin,
    SpacyNLPSequenceDoc2VecBuilderMixin
):
    pass
