from doc2vec.spacy.components.sentiment.cls import BasicSentiment

from .words import posiwords, negawords


class JapaneseLanguageSentiment(BasicSentiment):
    def __init__(self,):
        super().__init__(posiwords=posiwords, negwords=negawords)
        self.initialize()
