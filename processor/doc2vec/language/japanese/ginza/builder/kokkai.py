

from ..components.keyword_extractor.kokkai_rule import KokkaiExtractRules
from .base import SpacyGinzaJapaneseLanguageDoc2VecBuilderBase


class SpacyGinzaJapaneseLanguageDoc2VecBuilderKokkai(SpacyGinzaJapaneseLanguageDoc2VecBuilderBase):
    def __init__(self, rules=KokkaiExtractRules, stopword_rules=[], keyword_limit=5, chulknsize=25):
        super().__init__(rules, stopword_rules, keyword_limit)
        self.use_facade(chuknsize=chulknsize)
