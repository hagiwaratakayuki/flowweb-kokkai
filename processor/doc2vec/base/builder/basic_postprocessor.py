from typing import Type
from doc2vec.base.postprocessor.cls import Postprocessor
from doc2vec.base.keyword_extractor.basic import BasicKeywordExtractor
from doc2vec.base.protocol.vectorizer import Vectorizer
from doc2vec.base.protocol.sentiment import SentimentAnarizer


class Builder:
    sentiment_anarizer: SentimentAnarizer
    vectorizer: Vectorizer
    keyword_extractor: BasicKeywordExtractor
    postprocessor_class: Type[Postprocessor]

    def __init__(self, postprocessor_clsss=Postprocessor):
        self.postprocessor_class = postprocessor_clsss

    def build_postprocessor(self):
        return self.postprocessor_class(self.vectorizer, self.sentiment_anarizer, self.keyword_extractor)
