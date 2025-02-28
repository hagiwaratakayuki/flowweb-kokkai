from doc2vec.spacy.keyword_extracter.cls import BasicKeywordExtratcer
RULES = []


class JapaneseLanguageKeywordExtracter(BasicKeywordExtratcer):
    def __init__(self):
        super().__init__(RULES)
