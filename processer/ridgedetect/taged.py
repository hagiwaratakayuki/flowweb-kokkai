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
            tag_links = defaultdict(frozenset)

            for cluster_member in cluster_members:
                tags = self._tags_map[cluster_member]
                tags_set = set(tags)

                for tag in tags:
                    tag_links[tag] += tags_set - set([tag])

                    tag_2_members[tag].append(cluster_member)
            tag_2_members = {tag: frozenset(member)
                             for tag, member in tag_2_members}

            sub_clusters = defaultdict(deque)

            checked_links = defaultdict(set)
            tag_2_sub_clusters = defaultdict(dict)
            for tag, members in tag_2_members.items():
                linked_tags = tag_links[tag] - checked_links[tag]
                tag_set = set([tag])
                for linked_tag in linked_tags:
                    add_linked_tag = False
                    for target_clusters in [tag_2_sub_clusters[linked_tag], [tag_2_members[linked_tag]]]:

                        for target_cluster in target_clusters:
                            new_cluster = target_cluster & members
                            new_tags = sub_clusters[target_cluster].copy()
                            tag_2_sub_clusters[linked_tag][new_cluster] = True

                            new_tags.append(tag)
                            if add_linked_tag == True:
                                new_tags.append(linked_tag)
                            sub_clusters[new_cluster] = new_tags
                        add_linked_tag = True

                    checked_links[linked_tag] += tag_set

                sub_clusters[members].append(tag)

            for members, tags in sub_clusters.items():
                new_clusters[cluster_id] = members
                tag_index[cluster_id] = frozenset(tags)
                """
                for member in members:
                    member_to_clusters[member].append(cluster_id)
                """
                cluster_id += 1

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.member_to_clusters = member_to_clusters

        # self.member_to_clusters = {member: list(_clusters) for member, _clusters in member_to_clusters} /
