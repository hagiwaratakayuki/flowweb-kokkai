

from typing import Dict

import numpy as np
from numpy import ndarray
from utillib.random_projection import projection

CASH = {}
NORM_CACHE = {}


def project_vector(vectors: Dict[any, ndarray]):
    global CASH
    not_cached = [(key, vector)
                  for key, vector in vectors.items() if key not in CASH]
    if len(not_cached) == 0:
        return {key: CASH[key] for key in vectors.keys() if key in CASH}
    X = np.array([r[1] for r in not_cached])
    projected_vectors = projection(X=X)

    projected_dict = {r[0]: vector for r,
                      vector in zip(not_cached, projected_vectors)}
    ret = {key: CASH[key] for key in vectors.keys() if key in CASH}
    CASH.update(projected_dict)
    ret.update(projected_dict)
    return ret
