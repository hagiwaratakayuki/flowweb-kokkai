

import re
from typing import List, Type
from doc2vec.base.keyword_extractor.basic import BasicKeywordExtractor
from doc2vec.base.builder import basic_postprocessor
from doc2vec.base.protocol.sentiment import SentimentAnarizer
from doc2vec.base.vectorizer.gensim import Vectorizer
from doc2vec.base.sentiment.vector_sentiment import VectorSentiment


class BuilderClass(basic_postBuilder):
    sentiment_anarizer_class: Type[VectorSentiment] = VectorSentiment
    vectorizer_class: Type[Vectorizer] = Vectorizer
    keyword_extractor_class: Type[BasicKeywordExtractor] = BasicKeywordExtractor

    def __init__(self, postprocessor_clsss=basic_postPostprocessor, keyword_extractor_class=None, sentiment_anarizer_class=None, vectorizer_class=None) -> None:
        if keyword_extractor_class is not None:
            self.keyword_extractor_class = keyword_extractor_class
        if sentiment_anarizer_class is not None:
            self.sentiment_anarizer_class = sentiment_anarizer_class
        if vectorizer_class is not None:
            self.vectorizer_class = vectorizer_class
        super().__init__(postprocessor_clsss=postprocessor_clsss)

    def build_sentiment_anarizer(self, posi_words: List[str], nega_words: List[str]):
        self.sentiment_anarizer = self.sentiment_anarizer_class(
            posi_words=posi_words, nega_words=nega_words, vectorizer=self.vectorizer)
        return self

    def build_vectorizer(self, model_path=None, basepath='', loader=None):
        self.vectorizer = self.vectorizer_class(
            model_path=model_path, basepath=basepath, loader=loader)
        return self

    def build_keyword_extractor(self, rules, stopword_rules, keyword_limit=5, result_class=None):
        self.keyword_extractor = self.keyword_extractor_class(
            rules=rules, stopword_rules=stopword_rules, keyword_limit=keyword_limit, result_class=result_class, vectoraizer=self.vectorizer)
        return self
