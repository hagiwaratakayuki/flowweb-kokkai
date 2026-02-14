from csv import Error
from typing import TypedDict
from doc2vec.base.sentiment.builder_mixin.wordbase_sentiment.sequence_doc2vec.mixin import SequenceDoc2vecWordbaseSentimentMixin
from processor.doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.apply_mixin import SpacyNLPSequenceDoc2VecBuilderApplyMixin
from doc2vec.spacy.components.nlp.mixin import SpacyNLPMixin
from .cls import SpacyBasicSentiment


class SpacySentimentBuilderOptions(TypedDict):
    punct: str


class SpacySentimentBuilderMixin(SequenceDoc2vecWordbaseSentimentMixin, SpacyNLPSequenceDoc2VecBuilderApplyMixin):
    sentiment_class = SpacyBasicSentiment

    def use_wordbase_sentiment(self, posi_words, nega_words, model_name=None, init_param_key=None, options: SpacySentimentBuilderOptions = {}):
        kwargs = self._apply_model_configure(model_name, init_param_key)
        kwargs.update(options)

        return super().use_wordbase_sentiment(posi_words=posi_words, nega_words=nega_words, kwargs=kwargs)
