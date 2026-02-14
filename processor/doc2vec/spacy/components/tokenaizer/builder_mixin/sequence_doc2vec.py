from doc2vec.base.tokenaizer.builder_mixin.sequence_doc2vec.protocol import TokenaizerSequenceDoc2VecBuilderMixin


class SpacyTokenizerSequenceDoc2VecBuilderMixin(TokenaizerSequenceDoc2VecBuilderMixin):
    def use_tokenizer(self, model_name=None, init_param_key=None, kwargs={}):
        if model_name != None:
            self.model_name = model_name
        if init_param_key != None:
            self.init_param_key = init_param_key
        _model_name = model_name or self.model_name
        _init_param_key = init_param_key or self.init_param_key
        if _model_name == None:
            raise 'model_name is not set'
        if _init_param_key == None:
            raise 'init_param_key is not set'
        _kwargs = kwargs.copy()
        _kwargs[_init_param_key] = _model_name
        self.tokenizer_params.update(_kwargs)
        return self
