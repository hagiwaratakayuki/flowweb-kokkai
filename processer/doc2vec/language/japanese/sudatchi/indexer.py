from typing import Optional

import numpy as np
from doc2vec.base.indexer.cls import Indexer
from sudachipy.morpheme import Morpheme

from doc2vec.base.protocol.vectorizer import WordToVecDictType
from doc2vec.language.japanese.sudatchi.util import reguraize_rule
from processer.doc2vec.language.japanese.sudatchi.util.matcher.preset import adjective, counter_word, counter_word_possible, noun, number, verb

MainPos = noun.matcher | verb.matcher - \
    counter_word.matcher - counter_word_possible.matcher - number.matcher
SpecifiablePos = MainPos | adjective.matcher


class SudatchiIndexer(Indexer):

    def _check_specifiable_pos(self, token: Morpheme) -> bool:
        return SpecifiablePos(token)

    def _check_main_pos(self, token: Morpheme) -> bool:
        return MainPos(token)

    def _get_vector(self, word_to_vector: WordToVecDictType, token: Morpheme) -> Optional[np.ndarray]:
        return word_to_vector.get(self._get_reguraized(token=token))

    def _get_reguraized(self, token: Morpheme) -> str:
        return reguraize_rule.apply(token=token)
