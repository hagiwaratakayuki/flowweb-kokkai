

import ginza
from doc2vec.spacy.components.doc2vec import SpacyDoc2Vec
from doc2vec.spacy.japanese_language.components.const import MODEL_NAME
from doc2vec.spacy.japanese_language.components.keyword_extract.cls import JapaneseLanguageKeywordExtracter
from doc2vec.spacy.japanese_language.components.vectaizer.cls import JapaneseLanguageVectoraizer
from doc2vec.spacy.japanese_language.components.sentiment.cls import JapaneseLanguageSentiment


class BasicJapaneseLanguageDoc2Vec(SpacyDoc2Vec):
    def __init__(self, keyword_extracter=None, vectoraizer=None, sentiment=None, n_processes=None, batch_size=-1, spacy_cofing={}):
        name = MODEL_NAME
        delimiter = "\n\n"
        keyword_extracter = keyword_extracter or JapaneseLanguageKeywordExtracter()
        vectoraizer = vectoraizer or JapaneseLanguageVectoraizer()

        sentiment = sentiment or JapaneseLanguageSentiment()

        super().__init__(name=name, keyword_extracter=keyword_extracter, vectoraizer=vectoraizer, sentiment=sentiment, delimiter=delimiter, n_process=n_processes, batch_size=batch_size,
                         spacy_cofing=spacy_cofing)
        ginza.set_split_mode(nlp=self.nlp, mode="A")
