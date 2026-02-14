from turtle import mode

from doc2vec.spacy.components.nlp.builder_mixin.sequence_doc2vec.root import SpacyNLPSequenceDoc2VecBuilderMixinRoot


class SpacyNLPSequenceDoc2VecBuilderApplyMixin(SpacyNLPSequenceDoc2VecBuilderMixinRoot):

    def _apply_model_configure(self, model_name, init_param_key):
        if model_name != None:
            self.model_name = model_name
        if init_param_key != None:
            self.init_param_key = init_param_key
        _model_name = model_name or self.model_name
        _init_param_key = init_param_key or self.init_param_key
        self._validate_model_configure(_model_name, _init_param_key)

        kwargs = {}
        kwargs[_init_param_key] = _model_name
        return kwargs
