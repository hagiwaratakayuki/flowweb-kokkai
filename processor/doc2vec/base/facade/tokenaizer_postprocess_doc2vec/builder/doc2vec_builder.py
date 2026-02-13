from typing import Dict, List, Type

from fastapi import params

from doc2vec.base.facade.tokenaizer_postprocess_doc2vec.facade_class import Doc2Vec

from .root import TokenaizerPostprocessMixinRoot
from doc2vec.base.postprocessor.cls import Postprocessor
from doc2vec.base.protocol.postprocessor import AbstractPostprocessorCls
from doc2vec.base.protocol.tokenizer import AbstarctTokenizerClass


class TokenaierPostprocessorDoc2VecBuilder(TokenaizerPostprocessMixinRoot):

    doc2vec_class: Type[Doc2Vec] = Doc2Vec
    postprocessor_class: Type[AbstractPostprocessorCls] = Postprocessor
    tokennaizer_class: Type[AbstarctTokenizerClass]
    postprocessor_params: Dict
    tokenizer_params: Dict

    def _build(self, doc2vec_init={}):
        postprocesser = self._build_postprocessor()
        tokenaizer = self._build_tokenizer()
        self.postprocesser_filters = []
        self.tokenaizer_mixins = []

        return self.doc2vec_class(postprocesser=postprocesser, tokenaizer=tokenaizer, **doc2vec_init)

    def _build_postprocessor(self):

        params = self._call_filters(
            self.postprocesser_filters, self.postprocessor_params.copy())
        return self.postprocessor_class(**params)

    def _build_tokenizer(self):
        params = self._call_filters(
            self.tokenaizer_mixins, self.tokenizer_params.copy())
        return self.tokennaizer_class(**params)
