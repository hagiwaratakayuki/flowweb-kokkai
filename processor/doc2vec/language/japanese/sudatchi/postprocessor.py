from typing import Dict, Optional

from ginza import norm
import numpy as np
from doc2vec.base.postcls import Postprocessor
from sudachipy.morpheme import Morpheme

from doc2vec.base.protocol.vectorizer import WordToVecDictType
from doc2vec.language.japanese.sudatchi.util import reguraize_rule
from doc2vec.language.japanese.sudatchi.util.matcher.preset import adjective, counter_word, counter_word_possible, noun, number, verb

MainPos = (noun.matcher - counter_word.matcher -
           counter_word_possible.matcher - number.matcher) | verb.matcher

SpecifiablePos = MainPos | adjective.matcher


class SudatchiPostprocessor(Postprocessor):
    _reguraize_rule = reguraize_rule

    def _check_meanable_pos(self, token: Morpheme) -> bool:

        return SpecifiablePos(token)

    def _check_main_pos(self, token: Morpheme) -> bool:
        return MainPos(token)

    def _get_vector(self, word_to_vector: WordToVecDictType, token: Morpheme) -> Optional[np.ndarray]:
        return word_to_vector.get(self._get_reguraized(token=token))

    def _get_vector_length(self, word_to_vector_length: Dict[str, norm], token: Morpheme) -> Optional[float]:
        return word_to_vector_length.get(self._get_reguraized(token=token))

    def _get_reguraized(self, token: Morpheme) -> str:
        return self._reguraize_rule.apply(token=token)
