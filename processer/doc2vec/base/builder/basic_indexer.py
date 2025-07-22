from processer.doc2vec.base.indexer.cls import Indexer
from processer.doc2vec.base.protocol.vectorizer import Vectorizer
from processer.doc2vec.base.protocol.sentiment import SentimentAnarizer


class Builder:
    sentiment_anarizer: SentimentAnarizer
    vectorizer: Vectorizer
    indexer_class = Indexer

    def build_indexer(self):
        return self.indexer_class(self.vectorizer, self.sentiment_anarizer)
