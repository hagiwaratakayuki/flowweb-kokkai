from doc2vec.spacy.components.keyword_extracter.cls import BasicKeywordExtratcer
from doc2vec.spacy.japanese_language.components.keyword_extract.rule import complex_word, subword


BASIC_RULES = [complex_word.Rule()]
SUBWORD_RULES = [subword.Rule()]


class JapaneseLanguageKeywordExtracter(BasicKeywordExtratcer):
    def __init__(self, before_basic_rules=[], mid_in_basic2subword_rules=[], after_sahen_rules=[]):
        super().__init__(before_basic_rules + BASIC_RULES +
                         mid_in_basic2subword_rules + SUBWORD_RULES + after_sahen_rules)
