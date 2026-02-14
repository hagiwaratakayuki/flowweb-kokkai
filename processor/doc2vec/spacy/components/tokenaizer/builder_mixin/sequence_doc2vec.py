from doc2vec.base.tokenaizer.builder_mixin.sequence_doc2vec.protocol import TokenaizerSequenceDoc2VecBuilderMixin
from processor.doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.apply_mixin import SpacyNLPSequenceDoc2VecBuilderApplyMixin


class SpacyTokenizerSequenceDoc2VecBuilderMixin(TokenaizerSequenceDoc2VecBuilderMixin, SpacyNLPSequenceDoc2VecBuilderApplyMixin):
    def use_tokenizer(self, model_name=None, init_param_key=None, kwargs={}):
        _kwargs = self._apply_model_configure(model_name, init_param_key)
        _kwargs.update(kwargs)

        self.tokenizer_params.update(_kwargs)
        return self
