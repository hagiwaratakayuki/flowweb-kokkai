from turtle import mode, st
from typing import Optional


class SpacyNLPSequenceDoc2VecBuilderMixinRoot:
    model_name: Optional[str] = None
    init_param_key = 'model_name'

    def _validate_model_configure(self, model_name, init_param_key):

        if not model_name:
            raise Exception('model_name is not set')
        if not init_param_key:
            raise Exception('init_param_key is not set')
