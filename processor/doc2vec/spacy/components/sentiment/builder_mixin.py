from processor.doc2vec.base.sentiment.builder_mixin.wordbase_sentiment.sequence_doc2vec.mixin import SequenceDoc2vecWordbaseSentimentMixin
from .cls import SpacyBasicSentiment


class SpacySentimentBuilderMixin(SequenceDoc2vecWordbaseSentimentMixin):
    sentiment_class = SpacyBasicSentiment

    def use_wordbase_sentiment(self, posi_words, nega_words, nlp, punct=None):
        kwargs = dict(nlp=nlp)
        if punct != None:
            kwargs['punct'] = punct
        return super().use_wordbase_sentiment(posi_words=posi_words, nega_words=nega_words, **kwargs)
