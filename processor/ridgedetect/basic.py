import numpy as np
from collections import defaultdict
from .searcher import btree
DEFAULT_SEARCHER = btree.Searcher()


class RidgeDitect(object):
    def __init__(self, searcher=DEFAULT_SEARCHER):
        self._searcher = searcher

    def init(self):
        self.graph = {}

    def fit(self, vectors, sample=4):

        nearbys = self._searcher.search(vectors, sample)

        nearby_vectors = vectors[nearbys] - np.expand_dims(vectors, axis=1)

        nearby_penalties = np.sum(nearby_vectors ** 2, 2)

        nearby_lengths = nearby_penalties ** 0.5

        guide_vectors = np.einsum(
            'ijk,ij->ik', nearby_vectors, 1 / nearby_penalties)
        scores = np.einsum('ijk,ik -> ij', nearby_vectors, guide_vectors) / \
            (nearby_lengths * np.linalg.norm(guide_vectors, 2))
        sorted_args = np.argsort(scores, axis=1)[:, ::-1]
        sorted_nearbys = np.take_along_axis(nearbys, sorted_args, axis=1)
        connectable_map = dict(
            zip(*np.unique(sorted_nearbys[:, 0], return_counts=True)))
        masks = self._get_masks(sorted_nearbys, scores,
                                sorted_args, nearby_vectors, vectors, sample)

        self.graph = {ind: nearby[mask][0:min(connectable_map.get(ind, 2), sample, np.count_nonzero(
            mask))] for ind, mask, nearby in zip(range(vectors.shape[0]), masks, sorted_nearbys)}

        vectors_length = vectors.shape[0]

        reverse_nodes = defaultdict(dict)
        for node, towords in self.graph.items():
            for toword in towords:
                reverse_nodes[toword][node] = True

        checked = {}
        clusters = {}
        cluster_number = 0
        cluster = {}
        for node in range(vectors_length):
            if node in checked:

                continue

            cluster[node] = True
            is_next_exist = True
            targets = {node: True}

            while is_next_exist:
                next_targets = {}
                is_next_exist = False
                for target in targets:
                    cluster[target] = True
                    checked[target] = True
                    canditates = set()

                    canditates.update(self.graph.get(target, {}))
                    canditates.update(reverse_nodes.get(target, {}))

                    for canditate in canditates:
                        if canditate in checked:
                            continue
                        next_targets[canditate] = True
                        is_next_exist = True
                targets = next_targets
            self._process_cluster(cluster, clusters, cluster_number)
            cluster_number += 1
            cluster = {}

        self.clusters = clusters

    def _process_cluster(self, cluster, clusters, clusters_number):
        clusters[clusters_number] = np.array(list(cluster))

    def _get_masks(self, sorted_nearbys, scores, sorted_args, samples, nearby_vectors, vectors):
        return np.take_along_axis(scores, sorted_args, axis=1) >= 0
