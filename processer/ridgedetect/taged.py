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
        member_to_clusters = defaultdict(deque)

        for cluster_members in clusters.values():

            tag_2_members = defaultdict(deque)
            sub_clusters = defaultdict(deque)
            sub_tags = {}
            tag_2_tag = defaultdict(set)

            for cluster_member in cluster_members:
                tags = self._tags_map[cluster_member]
                tags_set = set(tags)
                for tag in tags:
                    tag_2_tag[tag].update(tags_set - {tag})
                    tag_2_members[tag].append(cluster_member)

            for tag, members in tag_2_members.items():
                members_set = frozenset(members)
                sub_clusters[members_set].append(tag)

            for tags in sub_clusters.values():
                tags_set = set(tags)

                sub_tags_set = set()
                for tag in tags_set:
                    sub_tags_set.update(tag_2_tag[tag])
                sub_tags_set.difference_update(tags_set)
                sub_tags[cluster_id] = sub_tags_set

                new_clusters[cluster_id] = members
                tag_index[cluster_id] = tags_set
                """
                for member in members:
                    member_to_clusters[member].append(cluster_id)
                """
                cluster_id += 1

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.sub_tags = sub_tags
        # self.member_to_clusters = member_to_clusters

        # self.member_to_clusters = {member: list(_clusters) for member, _clusters in member_to_clusters} /
