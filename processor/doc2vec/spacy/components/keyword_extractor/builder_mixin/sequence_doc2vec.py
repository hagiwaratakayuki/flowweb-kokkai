from typing import Dict
from doc2vec.base.keyword_extractor.builder_mixin.sequence_doc2vec.mixin import SequenceDoc2vecKeywordExtractorBuilderMixin
from doc2vec.spacy.components.keyword_extractor.cls import SpacyBasicKeywordExtractor
from processor.doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.apply_mixin import SpacyNLPSequenceDoc2VecBuilderApplyMixin


class SpacyKeywordExtractorSequenceDoc2VecBuilderMixin(SequenceDoc2vecKeywordExtractorBuilderMixin, SpacyNLPSequenceDoc2VecBuilderApplyMixin):
    keyword_extractor_class = SpacyBasicKeywordExtractor

    def use_keyword_extractor(self, rules, stopword_rules=[], keyword_limit=5, model_name=None, init_param_key=None, kwargs: Dict = {}):
        _kwargs = kwargs.copy()
        _kwargs.update(self._apply_model_configure(model_name, init_param_key))
        super().use_keyword_extractor(rules=rules, stopword_rules=stopword_rules,
                                      keyword_limit=keyword_limit, kwargs=_kwargs)
