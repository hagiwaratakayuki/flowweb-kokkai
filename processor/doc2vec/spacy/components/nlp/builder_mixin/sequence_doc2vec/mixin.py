from pyexpat import model
from .root import SpacyNLPSquenceDoc2VecBuilderMixinRoot


class SpacyNLPSquenceDoc2VecBuilderMixin(SpacyNLPSquenceDoc2VecBuilderMixinRoot):
    def set_model_configure(self, model_name, init_param_key='model_name'):
        if not model_name:
            raise 'model_name is not set'
        if not init_param_key:
            raise 'init_param_key is not set'
        self.model_name = model_name
        self.init_param_key = init_param_key
