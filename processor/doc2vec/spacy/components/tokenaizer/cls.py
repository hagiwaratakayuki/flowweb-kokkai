from typing import Any, Tuple
from doc2vec.base.protocol.tokenizer import AbstarctTokenizerClass
from ..nlp.mixin import SpacyNLPMixin


class SpacyToknaizer(AbstarctTokenizerClass, SpacyNLPMixin):
    def __init__(self, model_name):
        self._set_model_name(model_name)

    def parse(self, arg: Tuple[str, Any]):
        text, data_id = arg
        nlp = self._get_language()
        return nlp(text), data_id
