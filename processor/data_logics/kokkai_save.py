from collections import deque, defaultdict
from typing import Dict, Iterable, Tuple
from numpy import ndarray

from db.node import Node
from data_loader.kokkai import DTO
from db.util.chunked_batch_saver import ChunkedBatchSaver
from doc2vec.base.protocol.sentiment import SentimentResult
from .node_logic import NodeLogic
from .save import Logic
from db.node_kokkai import NodeKokkai
from db.kokkai_cluster import KokkaiCluster
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.kokkai_cluster_link import KokkaiClusterLink


class KokkaiNodeLogic(NodeLogic):
    session: int
    meeting_keywords: Dict[str, deque]

    def __init__(self, session, nodeModel: NodeKokkai = NodeKokkai, size: int = 30):
        self.session = session
        self._init_meeting_keywords()
        super().__init__(nodeModel, size=size)

    def _init_meeting_keywords(self):
        self.meeting_keywords = defaultdict(deque)

    def set_vectors(self, sentiment_result: SentimentResult):
        return super().set_vectors(sentiment_result)

    def setEntityProperty(self, entity, dto: DTO, nodeEntity: NodeKokkai, vector, link_to, linked_count, sentiment, keywords, is_apex_flag):
        ret = super().setEntityProperty(entity, dto, nodeEntity,
                                        vector, link_to, linked_count, sentiment, keywords, is_apex_flag)

        nodeEntity.session = self.session
        nodeEntity.house = dto.house
        nodeEntity.comittie = dto.comittie
        if dto.group != None:
            nodeEntity.group = dto.group
        self.meeting_keywords[dto.meeting_id].append(
            (nodeEntity.weight, nodeEntity.keywords,))

        return ret

    def get_meeting_keywords(self):
        ret = self.meeting_keywords
        self._init_meeting_keywords()
        return ret


class KokkaiLogic(Logic):
    def __init__(self, session, link_map, cluster_links_batch: ChunkedBatchSaver) -> None:
        self.session = session
        self._link_map = link_map
        self._next_link = defaultdict(deque)
        self._cluster_links_batch = cluster_links_batch

        super().__init__(ClusterModelClass=KokkaiCluster)

    def save(self, datas: Iterable[Tuple[ndarray, SentimentResult, Iterable[str], DTO]], nodeLogic: KokkaiNodeLogic):
        super().save(datas, nodeLogic=nodeLogic)

        self._link_map.update(self._next_link)
        return self._link_map, nodeLogic

    def _get_cluster_model(self, taged, innerid, cluster_members, weight_map: Dict, index2id: Dict):
        cluster_model = super()._get_cluster_model(
            taged, innerid, cluster_members, weight_map, index2id)
        cluster_model.session = self.session
        return cluster_model

    def _put_cluster_data(self, entities, members_chunk, cluster_keyword_chunk, index2id, linked_counts_map, member_model_chunk: ChunkedBatchSaver, index2published, taged, keyword_model_chunk: ChunkedBatchSaver, member_positions_chunk: deque, weight_map: Dict):
        super()._put_cluster_data(entities, members_chunk, cluster_keyword_chunk, index2id, linked_counts_map,
                                  member_model_chunk, index2published, taged, keyword_model_chunk, member_positions_chunk, weight_map)
        for entity, keywords in zip(entities, cluster_keyword_chunk):
            eid = entity.key.id_or_name
            keywords_fset = frozenset(keywords)
            self._next_link[keywords_fset].append((self.session, eid,))
            if keywords_fset in self._link_map:

                for session, cluster_id in self._link_map[keywords_fset]:

                    link_model = KokkaiClusterLink()
                    if session > self.session:
                        link_model.from_cluster = eid
                        link_model.to_cluster = cluster_id
                    else:
                        link_model.to_cluster = eid
                        link_model.from_cluster = cluster_id
                    self._cluster_links_batch.put(link_model, False)
