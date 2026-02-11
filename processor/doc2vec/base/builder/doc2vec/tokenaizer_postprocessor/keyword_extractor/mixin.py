from processor.doc2vec.base.builder.doc2vec.tokenaizer_postprocessor.root import TokenaizerPostprocessMixinRoot


class KeywordExtractorMixin(TokenaizerPostprocessMixinRoot):
    def use_keyword_extractor(self, rules, stopword_rules, keyword_limit=5):
        self.postprocesser_filters
