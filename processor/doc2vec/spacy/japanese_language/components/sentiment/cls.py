from doc2vec.spacy.components.sentiment.cls import SpacyBasicSentiment

from .words import posiwords, negawords


class JapaneseLanguageSentiment(SpacyBasicSentiment):
    def __init__(self,):
        super().__init__(posiwords=posiwords, negwords=negawords)
        self.initialize()
