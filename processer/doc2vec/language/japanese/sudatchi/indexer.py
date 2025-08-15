from typing import Optional

import numpy as np
from doc2vec.base.indexer.cls import Indexer
from sudachipy.morpheme import Morpheme

from doc2vec.base.protocol.vectorizer import WordToVecDictType
from doc2vec.language.japanese.sudatchi.util import reguraize_rule

MainPos = {'名詞', '動詞'}
SpecifiablePos = MainPos | {'形容詞'}


class SudatchiIndexer(Indexer):

    def _check_specifiable_pos(self, token: Morpheme) -> bool:
        return token.part_of_speech()[0] in SpecifiablePos

    def _check_main_pos(self, token: Morpheme) -> bool:
        return token.part_of_speech()[0] in MainPos

    def _get_vector(self, word_to_vector: WordToVecDictType, token: Morpheme) -> Optional[np.ndarray]:
        return word_to_vector.get(self._get_reguraized(token=token))

    def _get_reguraized(self, token: Morpheme) -> str:
        return reguraize_rule.apply(token=token)
