from doc2vec.spacy.components.keyword_extracter.cls import BasicKeywordExtratcer
from doc2vec.spacy.japanese_language.components.keyword_extract.rule import basic_word


BASIC_RULES = [basic_word.Rule()]


class JapaneseLanguageKeywordExtracter(BasicKeywordExtratcer):
    def __init__(self, before_basic_rules=[], after_basic_rules=[]):
        super().__init__(before_basic_rules + BASIC_RULES + after_basic_rules)
