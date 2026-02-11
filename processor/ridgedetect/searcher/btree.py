from sklearn.neighbors import BallTree
import numpy as np

class Searcher(object):
    leaf_size:int
    metric:str
    kwargs:dict
    def __init__(self, leaf_size=40, metric='minkowski', **kwargs) -> None:
        self.leaf_size = leaf_size
        self.metric = metric
        self.kwargs = kwargs
    def search(self, vectors, sample) -> np.ndarray:
        tree = BallTree(vectors, self.leaf_size, metric=self.metric, **self.kwargs)
        return tree.query(vectors, sample + 1, return_distance=False)[:,1:sample+1] # type: ignore
