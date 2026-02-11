from data_loader.kokkai import DTO
from .cls import JapaneseLanguageKeywordExtractor
from .rule.kokkai import comittie, lawname
RULES = [comittie.Rule(), lawname.Rule()]


class KokkaiKeywordExtractor(JapaneseLanguageKeywordExtractor):
    def __init__(self, before_basic_rules=[], after_basic_rules=[]):

        super().__init__(before_basic_rules=before_basic_rules,
                         after_basic_rules=RULES + after_basic_rules)

    def _get_text(self, dto: DTO):
        return dto.body
