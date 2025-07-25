

from typing import List
from doc2vec.base.keyword_extracter.basic import BasicKeywordExtratcer
from doc2vec.base.builder import basic_indexer
from doc2vec.base.protocol.sentiment import SentimentAnarizer
from doc2vec.base.vectorizer.gensim import Vectorizer


class BuilderClass(basic_indexer.Builder):
    sentiment_anarizer_class = SentimentAnarizer
    vectorizer_class = Vectorizer
    keyword_extracter_class = BasicKeywordExtratcer

    def build_sentiment_anarizer(self, posi_words: List[str], nega_words: List[str]):
        self.sentiment_anarizer = self.sentiment_anarizer_class(
            posi_words=posi_words, nega_words=nega_words)
        return self

    def buide_vectorizer(self, filepath=None, basepath='', loader=None):
        self.vectorizer = self.vectorizer_class(
            filepath=filepath, basepath=basepath, loader=loader)
        return self

    def build_keyword_extracter(self, rules, keyword_limit=5):
        self.keyword_extracter = self.keyword_extracter_class(
            rules=rules, keyword_limit=keyword_limit)
        return self
