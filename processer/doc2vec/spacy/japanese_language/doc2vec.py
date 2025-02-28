

from processer.doc2vec.spacy.doc2vec import SpacyDoc2Vec
from processer.doc2vec.spacy.japanese_language.const import MODEL_NAME
from processer.doc2vec.spacy.japanese_language.keyword_extract import JapaneseLanguageKeywordExtracter
from processer.doc2vec.spacy.japanese_language.sentiment import JapaneseLanguageSentiment


class JapaneseLangugageDoc2Vec(SpacyDoc2Vec):
    def __init__(self, batch_size=50, spacy_cofing={}):
        name = MODEL_NAME
        keyword_extracter = JapaneseLanguageKeywordExtracter()
        delimiter = "。\n"
        sentiment = JapaneseLanguageSentiment()
        super().__init__(name, keyword_extracter, sentiment, delimiter)
