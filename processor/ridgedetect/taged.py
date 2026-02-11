
from multiprocessing.pool import Pool

from typing import Dict, Optional


from .basic import RidgeDitect
import numpy as np
from collections import Counter, defaultdict, deque
from itertools import combinations
import uuid
EMPTY_FROZEN_SET = frozenset()
EMPTY_SET = set()


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

        cluster_link = defaultdict(deque)

        if pool != None:
            maped = pool.imap_unordered(
                func=self._mapper, iterable=clusters.values(), chunksize=chunksize)

        else:
            maped = (self._mapper(cluster_members=cluster_members)
                     for cluster_members in clusters.values())
        for _tag_index, _cluster_link, _new_clusters in maped:
            tag_index.update(_tag_index)
            cluster_link.update(_cluster_link)
            new_clusters.update(_new_clusters)

        self.clusters = new_clusters
        self.tag_index = tag_index
        self.cluster_link = cluster_link

    def _mapper(self, cluster_members):
        global EMPTY_FROZEN_SET
        tag_index = {}

        cluster_link = defaultdict(dict)
        new_clusters = {}
        tag_member_map = defaultdict(deque)

        sub_clusters = defaultdict(set)
        tag_paires = defaultdict(set)

        for cluster_member in cluster_members:
            tags = self._tags_map[cluster_member]

            for tag in tags:

                tag_member_map[tag].append(cluster_member)

            if len(tags) > 1:
                for tag_a, tag_b in combinations(tags, 2):
                    tag_paires[tag_a].add(tag_b)
                    tag_paires[tag_b].add(tag_a)

        tag_member_map_frozen = {tag: frozenset(
            members) for tag, members in tag_member_map.items()}

        for tag, init_members in tag_member_map_frozen.items():
            step_sub_clusters = {}
            ftgset = frozenset([tag])
            sub_clusters[init_members] |= ftgset

            step_tags_deque = deque([(ftgset, init_members, tag,)])
            is_link_tag_exist = True

            while is_link_tag_exist == True:
                next_step_tags_deque = deque()

                is_link_tag_exist = False
                step_member_check = {}
                for step_tags, step_members, connecter_tag in step_tags_deque:

                    for link_tag in tag_paires.get(connecter_tag, EMPTY_SET) - step_tags:

                        next_tags = step_tags | frozenset([link_tag])

                        members_set = tag_member_map_frozen[link_tag] & step_members

                        if members_set == EMPTY_FROZEN_SET or (members_set in sub_clusters):
                            continue

                        if members_set in step_member_check:
                            continue

                        step_member_check[members_set] = next_tags
                        is_link_tag_exist = True
                        next_step_tags_deque.append(
                            (next_tags, members_set, link_tag,))
                step_sub_clusters.update(step_member_check)
                step_tags_deque = next_step_tags_deque
            for members, tags in step_sub_clusters.items():
                sub_clusters[members] |= tags

        tag2subclsuter = defaultdict(deque)
        for members, tags in sub_clusters.items():

            subcluster_id = uuid.uuid4().hex
            new_clusters[subcluster_id] = members
            tag_index[subcluster_id] = tags
            for tag in tags:

                tag2subclsuter[tag].append(subcluster_id)
        links_set = set()
        for canditates in tag2subclsuter.values():
            if len(canditates) <= 1:
                continue
            for paire in combinations(canditates, 2):
                links_set.add(frozenset(paire))

        for start, target in links_set:
            start_members = new_clusters[start]
            target_members = new_clusters[target]

            cross_set = start_members & target_members

            cross_count = len(cross_set)
            if cross_count == 0:
                continue
            cluster_link[start][target] = cross_count
            cluster_link[target][start] = cross_count

        return tag_index, cluster_link, new_clusters
