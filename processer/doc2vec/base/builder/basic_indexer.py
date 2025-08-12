from typing import Type
from doc2vec.base.indexer.cls import Indexer
from doc2vec.base.keyword_extracter.basic import BasicKeywordExtratcer
from doc2vec.base.protocol.vectorizer import Vectorizer
from doc2vec.base.protocol.sentiment import SentimentAnarizer


class Builder:
    sentiment_anarizer: SentimentAnarizer
    vectorizer: Vectorizer
    keyword_extratcer: BasicKeywordExtratcer
    indexer_class: Type[Indexer]

    def __init__(self, indexer_clsss=Indexer):
        self.indexer_class = indexer_clsss

    def build_indexer(self):
        return self.indexer_class(self.vectorizer, self.sentiment_anarizer, self.keyword_extratcer)
