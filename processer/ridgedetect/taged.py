
from multiprocessing.pool import Pool
from typing import Dict, Optional
from .basic import RidgeDitect
import numpy as np
from collections import defaultdict, deque
from itertools import combinations
import uuid
EMPTY_SET = frozenset([])


class Taged(RidgeDitect):
    def fit(self, tags_map: dict, vectors: np.ndarray, sample=4, pool: Optional[Pool] = None):
        self._tags_map = tags_map

        ret = super().fit(vectors, sample)

        self._postprocess(self.clusters, pool)
        return ret

    def _get_masks(self, nearbys, scores, sorted_args, samples, nearby_vectors, vectors):
        tags_array = np.array([set(tags) for tags in self._tags_map.values()])
        nearby_tags = tags_array[nearbys]
        ret = (nearby_tags.T & tags_array.T).astype(bool).T

        return ret

    def _postprocess(self, clusters: Dict, pool: Optional[Pool] = None, chunksize=1):

        tag_index = {}

        new_clusters = {}
        cluster_id = 0
        cluster_link = defaultdict(deque)

        if pool != None:
            maped = pool.imap_unordered(
                func=self._mapper, iterable=clusters.values(), chunksize=chunksize)

        else:
            maped = (self._mapper(cluster_members=cluster_members)
                     for cluster_members in clusters.values())
        for _tag_index, _cluster_link,  _new_clusters in maped:
            tag_index.update(_tag_index)
            cluster_link.update(_cluster_link)
            new_clusters.update(_new_clusters)

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.cluster_link = cluster_link

    def _mapper(self, cluster_members):
        global EMPTY_SET
        tag_index = {}

        cluster_link = defaultdict(dict)
        new_clusters = {}
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
        tag2subclsuter = defaultdict(deque)
        for members, tags in sub_clusters.items():
            subcluster_id = uuid.uuid4().hex
            new_clusters[subcluster_id] = members
            tag_index[subcluster_id] = tags
            for tag in tag2subclsuter:

                tag2subclsuter[tag].append(subcluster_id)
        links_set = set([frozenset(paire) for paire in [combinations(
            canditates, 2) for canditates in tag2subclsuter.values()]])
        for start, target in links_set:
            start_members = new_clusters[start]
            target_members = new_clusters[target]

            cross_set = start_members & target_members

            cross_count = len(cross_set)
            cluster_link[start][target] = cross_count
            cluster_link[target][start] = cross_count

        return tag_index, cluster_link,  new_clusters
