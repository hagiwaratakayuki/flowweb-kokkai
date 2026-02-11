from typing import Dict
from processor.doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter


class WordbaseSentimentFilter(AbstractFilter):
    def __init__(self, posi_words, nega_words, arg_keyword='sentiment_anarizer'):
        self.posi_words = posi_words
        self.nega_words = nega_words
        self.arg_keyword = arg_keyword

    def execute(self, params: Dict) -> Dict:
        params[self.arg_keyword] = self._build_sntiment_anarizer()
        return params

    def _build_sntiment_anarizer(self):
        pass
