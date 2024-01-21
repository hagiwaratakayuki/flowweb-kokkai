
from sklearn.random_projection import SparseRandomProjection
import numpy as np
import scipy as sp
import os


DUMMY_ARR = np.zeros((2, 300), dtype=float)
DUMMY_G = SparseRandomProjection(n_components=2)
DUMMY_G.fit_transform(DUMMY_ARR)

projection_matrix = DUMMY_G.components_.T
path = os.path.join(os.path.dirname(__file__), './random_mat.npz')
sp.sparse.save_npz(path, projection_matrix)
