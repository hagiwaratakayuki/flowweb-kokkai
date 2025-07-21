from typing import Any, Dict

import numpy as np


WordToVecDictType = Dict[str, np.ndarray]


class Vectorizer:
    def get_vectors(self, words) -> Dict[str, np.ndarray]:
        pass
