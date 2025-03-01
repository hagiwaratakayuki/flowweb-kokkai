

from doc2vec.spacy.doc2vec import SpacyDoc2Vec
from doc2vec.spacy.japanese_language.const import MODEL_NAME
from doc2vec.spacy.japanese_language.keyword_extract import JapaneseLanguageKeywordExtracter
from doc2vec.spacy.japanese_language.sentiment import JapaneseLanguageSentiment


class BasicJapaneseLangugageDoc2Vec(SpacyDoc2Vec):
    def __init__(self, keyword_extracter=JapaneseLanguageKeywordExtracter(), batch_size=50, spacy_cofing={}):
        name = MODEL_NAME
        delimiter = "。\n"
        sentiment = JapaneseLanguageSentiment()
        super().__init__(name, keyword_extracter, sentiment, delimiter,
                         batch_size=batch_size, spacy_cofing=spacy_cofing)
