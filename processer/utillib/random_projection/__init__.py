from .dot import safe_sparse_dot
import scipy as sp
import os

path = os.path.join(os.path.dirname(__file__), './random_mat.npz')
projection_matrix = sp.sparse.load_npz(path)


def projection(X):
    return safe_sparse_dot(X, projection_matrix)
