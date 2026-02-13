from typing import List

from doc2vec.base.builder.components.mixins.filter.protocol import AbstractFilter
from doc2vec.base.builder.components.mixins.use_filter import UseFilterMixin


class TokenaizerPostprocessMixinRoot(UseFilterMixin):
    postprocesser_filters: List[AbstractFilter]
    tokenaizer_filters: List[AbstractFilter]
