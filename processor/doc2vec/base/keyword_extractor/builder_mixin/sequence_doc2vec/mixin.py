from doc2vec.base.facade.sequence_doc2vec.builder.root import SequenceDoc2VecBuilderRoot


class SequenceDoc2vecKeywordExtractorBuilderMixin(SequenceDoc2VecBuilderRoot):
    def use_keyword_extractor(self, rules, stopword_rules=[], keyword_limit=5, kwargs={}):
        self.keyword_extractor_params.update(
            rules=rules,
            stopword_rules=stopword_rules,
            keyword_limit=keyword_limit,
            **kwargs
        )
        return self
