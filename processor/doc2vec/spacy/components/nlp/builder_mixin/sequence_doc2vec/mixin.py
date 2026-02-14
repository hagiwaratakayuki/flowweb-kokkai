from pyexpat import model
from .root import SpacyNLPSequenceDoc2VecBuilderMixinRoot


class SpacyNLPSequenceDoc2VecBuilderMixin(SpacyNLPSequenceDoc2VecBuilderMixinRoot):
    def set_model_configure(self, model_name, init_param_key='model_name'):
        self._validate_model_configure(model_name, init_param_key)
        self.model_name = model_name
        self.init_param_key = init_param_key
