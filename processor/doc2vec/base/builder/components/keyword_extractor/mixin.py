from typing import Type
from doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter
from doc2vec.base.builder.doc2vec.tokenaizer_postprocessor.root import TokenaizerPostprocessMixinRoot


class KeywordExtractorMixin(TokenaizerPostprocessMixinRoot):
    filter_class: Type[AbstractFilter]

    def use_keyword_extractor(self, rules, stopword_rules, keyword_limit=5, kwargs={}):
        self.postprocesser_filters.append(self.filter_class(
            rules=rules, stopword_rules=stopword_rules, keyword_limit=keyword_limit, **kwargs))
