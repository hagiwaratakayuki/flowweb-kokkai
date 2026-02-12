from typing import Any, Dict, Tuple

import numpy as np


WordToVecDictType = Dict[str, np.ndarray]


class WordVectorizer:
    def get_vectors(self, words) -> Tuple[Dict[str, np.ndarray], Dict[str, float]]:
        pass
