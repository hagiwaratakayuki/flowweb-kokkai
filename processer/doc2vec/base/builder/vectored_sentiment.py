

from typing import List
from processer.doc2vec.base.builder import basic_indexer
from processer.doc2vec.base.protocol.sentiment import SentimentAnarizer
from processer.doc2vec.base.vectorizer.gensim import Vectaizer


class BuilderClass(basic_indexer.Builder):
    sentiment_anarizer_class = SentimentAnarizer
    vectorizer_class = Vectaizer

    def build_sentiment_anarizer(self, posi_words: List[str], nega_words: List[str]):
        self.sentiment_anarizer = self.sentiment_anarizer_class(
            posi_words=posi_words, nega_words=nega_words)
        return self

    def buide_vectorizer(self, filepath=None, basepath='', loader=None):
        self.vectorizer = self.vectorizer_class(
            filepath=filepath, basepath=basepath, loader=loader)
        return self
