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
        member_to_clusters = defaultdict(deque)

        for cluster_members in clusters.values():

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
                """
                for member in members:
                    member_to_clusters[member].append(cluster_id)
                """
                cluster_id += 1

        self.clusters = new_clusters
        self.tag_index = tag_index

        # self.sub_tags = sub_tags
        # self.member_to_clusters = member_to_clusters

        # self.member_to_clusters = {member: list(_clusters) for member, _clusters in member_to_clusters} /
