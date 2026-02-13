

from typing import Any
from doc2vec.base.facade.sequence_doc2vec.builder.root import SequenceDoc2VecBuilderRoot


class SequenceDoc2vecWordbaseSentimentMixin(SequenceDoc2VecBuilderRoot):
    sentiment_class: Any

    def use_wordbase_sentiment(self, posi_words, nega_words, arg_keyword='sentiment', kwargs={}):
        self.document_vectoraier_params[arg_keyword] = self._build_sentiment(
            posi_words=posi_words, nega_words=nega_words, **kwargs)
        return self

    def _build_sentiment(self, **kwargs):
        return self.sentiment_class(**kwargs)
