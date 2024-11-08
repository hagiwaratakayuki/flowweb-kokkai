from processer import cluster
from .basic import RidgeDitect
import numpy as np
from collections import defaultdict, deque
from itertools import combinations


class Taged(RidgeDitect):
    def fit(self, tags_map: dict, vectors: np.ndarray, sample=4):
        self._tags_map = tags_map

        ret = super().fit(vectors, sample)

        self._postprocess(self.clusters)
        return ret

    def _get_masks(self, nearbys, scores, sorted_args, samples, nearby_vectors, vectors):
        tags_array = np.array([set(tags) for tags in self._tags_map.values()])
        nearby_tags = tags_array[nearbys]
        ret = (nearby_tags.T & tags_array.T).astype(bool).T

        return ret

    def _postprocess(self, clusters):

        tag_index = {}

        new_clusters = {}
        cluster_id = 0
        cluster_link = defaultdict(deque)
        empty_set = frozenset([])
        for cluster_members in clusters.values():
            cluster_group_id = 0
            cluster_group = {}
            tags_2_members = defaultdict(deque)
            sub_clusters = defaultdict(set)

            for cluster_member in cluster_members:
                tags = self._tags_map[cluster_member]

                for i in range(1, len(tags) + 1):
                    for combination in combinations(tags, i):
                        tags_2_members[frozenset(combination)].append(
                            cluster_member)

            for tags, members in tags_2_members.items():
                members_set = frozenset(members)
                sub_clusters[members_set].update(tags)

            for members, tags in sub_clusters.items():

                new_clusters[cluster_id] = members
                tag_index[cluster_id] = tags
                cluster_group[cluster_group_id] = cluster_id
                cluster_group_id += 1
                cluster_id += 1
            for cgid in range(cluster_group_id):
                cid = cluster_group[cgid]
                gmember = new_clusters[cid]
                for gtid in range(cgid + 1, cluster_group_id):
                    tid = cluster_group[gtid]
                    cross_set = gmember & new_clusters[tid]
                    if cross_set == empty_set:
                        continue
                    cross_count = len(cross_set)
                    cluster_link[cid].append((tid, cross_count,))
                    cluster_link[tid].append((cid, cross_count, ))

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.cluster_link = cluster_link
