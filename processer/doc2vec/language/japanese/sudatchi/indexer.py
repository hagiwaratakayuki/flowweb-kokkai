from typing import Optional

import numpy as np
from processer.doc2vec.base.indexer.cls import Indexer
from sudachipy.morpheme import Morpheme

from processer.doc2vec.base.protocol.vectorizer import WordToVecDictType

MainPos = {'名詞', '動詞'}
SpecifiablePos = MainPos | {'形容詞'}


class SudatchiIndexer(Indexer):

    def _check_specifiable_pos(self, token: Morpheme) -> bool:
        return token.part_of_speech()[0] in SpecifiablePos

    def _check_main_pos(self, token: Morpheme) -> bool:
        return token.part_of_speech()[0] in MainPos

    def _get_vector(self, word_to_vector: WordToVecDictType, token: Morpheme) -> Optional[np.ndarray]:
        return word_to_vector.get(self._get_norm())

    def _get_norm(self, token: Morpheme) -> str:
        surface = token.surface()
        if not surface.isascii():
            return token.normalized_form()
        return surface
