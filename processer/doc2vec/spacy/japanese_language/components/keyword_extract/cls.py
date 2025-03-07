from doc2vec.spacy.components.keyword_extracter.cls import BasicKeywordExtratcer
from doc2vec.spacy.japanese_language.components.keyword_extract.rule import noun, complex_word


BASIC_RULES = [noun.Rule(), complex_word.Rule()]
SAHEN_RULES = []


class JapaneseLanguageKeywordExtracter(BasicKeywordExtratcer):
    def __init__(self, before_basic_rules=[], mid_in_basic2sahen_rules=[], after_sahen_rules=[]):
        super().__init__(before_basic_rules + BASIC_RULES +
                         mid_in_basic2sahen_rules + SAHEN_RULES + after_sahen_rules)
