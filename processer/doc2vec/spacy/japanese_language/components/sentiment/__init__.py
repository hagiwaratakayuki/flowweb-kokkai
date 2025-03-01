from doc2vec.spacy.components.vectaizer.sentiment import BasicSentiment
from doc2vec.spacy.japanese_language.components.const import MODEL_NAME
from .words import posiwords, negawords


class JapaneseLanguageSentiment(BasicSentiment):
    def __init__(self):
        name = MODEL_NAME
        super().__init__(posiwords=posiwords, negwords=negawords, name=name)
