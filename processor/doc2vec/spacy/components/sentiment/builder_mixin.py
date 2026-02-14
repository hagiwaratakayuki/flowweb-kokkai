from csv import Error
from typing import TypedDict
from doc2vec.base.sentiment.builder_mixin.wordbase_sentiment.sequence_doc2vec.mixin import SequenceDoc2vecWordbaseSentimentMixin
from doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.root import SpacyNLPSquenceDoc2VecBuilderMixinRoot
from doc2vec.spacy.components.nlp.mixin import SpacyNLPMixin
from .cls import SpacyBasicSentiment


class SpacySentimentBuilderOptions(TypedDict):
    punct: str


class SpacySentimentBuilderMixin(SequenceDoc2vecWordbaseSentimentMixin, SpacyNLPSquenceDoc2VecBuilderMixinRoot):
    sentiment_class = SpacyBasicSentiment

    def use_wordbase_sentiment(self, posi_words, nega_words, model_name=None, init_param_key=None, options: SpacySentimentBuilderOptions = {}):
        if model_name != None:
            self.model_name = model_name
        if init_param_key != None:
            self.init_param_key = init_param_key

        if _model_name == None:
            raise 'model_name is not set'
        _model_name = model_name or self.model_name
        if _init_param_key == None:
            raise 'init_param_key is not set'
        _init_param_key = init_param_key or self.init_param_key

        kwargs = {}
        kwargs[_init_param_key] = _model_name
        kwargs.update(options)

        return super().use_wordbase_sentiment(posi_words=posi_words, nega_words=nega_words, kwargs=kwargs)
