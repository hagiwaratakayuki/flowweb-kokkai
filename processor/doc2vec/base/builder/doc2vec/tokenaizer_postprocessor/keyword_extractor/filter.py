from tracemalloc import stop
from typing import Any, Dict
from processor.doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter
from processor.doc2vec.spacy.japanese_language.components import keyword_extract


class KeywordExtractorFilter(AbstractFilter):
    keyword_extractor_class: Any

    def __init__(self, rules, stopword_rules, keyword_limit=5, arg_keyword='keyword_extractor', kwargs={}) -> None:
        self.rules = rules
        self.stopword_rules = stopword_rules
        self.keyword_limit = keyword_limit
        self.kwargs = kwargs
        self.arg_keyword = arg_keyword

    def execute(self, params: Dict) -> Dict:
        params[self.arg_keyword] = self._build_keyword_extarcor()
        return params

    def _build_keyword_extarcor(self):
        initargs = dict(rules=self.rules, stopword_rules=self.stopword_rules,
                        keyword_limit=self.keyword_limit)
        initargs.update(self.kwargs)
        return self.keyword_extractor_class(**initargs)
