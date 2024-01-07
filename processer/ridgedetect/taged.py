from .basic import RidgeDitect
import numpy as np
from collections import defaultdict, deque


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
        member_to_clusters = defaultdict(dict)
        for cluster_members in clusters.values():
            tag_2_members = defaultdict(deque)

            for cluster_member in cluster_members:
                tags = self._tags_map[cluster_member]

                for tag in tags:

                    tag_2_members[tag].append(member)
            sub_clusters = defaultdict(deque)
            for tag, members in tag_2_members.items():
                member_set = frozenset(members)
                for sub_member_set in sub_clusters.keys():
                    canditate_members = member_set & sub_member_set
                    if len(canditate_members) == 0:
                        continue
                    sub_clusters[canditate_members].append(tag)
                sub_clusters[member_set].append(tag)

            for members, tags in sub_clusters.items():
                new_clusters[cluster_id] = members
                tag_index[cluster_id] = tags
                for member in members:
                    member_to_clusters[member][cluster_id] = True
                cluster_id += 1

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.member_to_clusters = member_to_clusters

        # self.member_to_clusters = {member: list(_clusters) for member, _clusters in member_to_clusters} /
