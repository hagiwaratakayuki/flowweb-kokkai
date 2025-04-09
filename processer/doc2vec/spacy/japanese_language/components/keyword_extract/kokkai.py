from .cls import JapaneseLanguageKeywordExtracter
from .rule.kokkai import comittie
RULES = [comittie.Rule()]


class KokkaiKeywordExtracter(JapaneseLanguageKeywordExtracter):
    def __init__(self, before_basic_rules=[], after_basic_rules=[]):

        super().__init__(before_basic_rules=before_basic_rules,
                         after_basic_rules=RULES + after_basic_rules)
