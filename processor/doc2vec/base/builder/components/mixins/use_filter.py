from typing import Dict, List
from doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter


class UseFilterMixin:
    def _call_filters(self, mixins: List[AbstractFilter], params: Dict):

        for mixin in mixins:
            params = mixin.execute(params)
        return params
