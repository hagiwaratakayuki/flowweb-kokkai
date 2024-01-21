import sys
from sklearn.random_projection import SparseRandomProjection, GaussianRandomProjection
import numpy as np


# dummy data
X = np.zeros((2, 10), dtype=float)
print(X)
g = SparseRandomProjection(n_components=2)
g.fit_transform(X)

# random mat, transpose() from (out_d, int_d) to (in_d, out_d)
random_mat = g.components_.transpose()
print(random_mat.dot(X))
