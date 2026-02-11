from typing import Iterable
from sudachipy.morpheme import Morpheme
from doc2vec.base.keyword_extractor.basic import BasicKeywordExtractor
from doc2vec.language.japanese.sudatchi.util import reguraize_rule


class SudatchiKeywordExtarctor(BasicKeywordExtractor):
    _reguraize_rule = reguraize_rule

    def _get_score_keys(self, sorce_ids: Iterable[Morpheme]):
        return {self._reguraize_rule.apply(token=token) for token in sorce_ids}
