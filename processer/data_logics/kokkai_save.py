from collections import deque, defaultdict
from typing import Iterable
from numpy import ndarray

from processer.db.node import Node
from data_loader.kokkai import DTO
from processer.db.util.chunked_batch_saver import ChunkedBatchSaver
from processer.doc2vec.indexer.dto import SentimentResult
from .save import Logic, NodeModel
from db.node_kokkai import NodeKokkai
from db.kokkai_cluster import KokkaiCluster
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.cluster_link import ClusterLink


class KokkaiNodeModel(NodeModel):
    session: int

    def __init__(self, session, nodeModel: NodeKokkai, size: int = 30):
        self.session = session
        super().__init__(nodeModel, size)

    def setEntityProperty(self, dto: DTO, speech_node: NodeKokkai, vector: ndarray, link_to, linked_count, sentiment):
        super().setEntityProperty(dto, speech_node,
                                  vector, link_to, linked_count, sentiment)
        speech_node.session = self.session


class KokkaiLogic(Logic):
    def __init__(self, session, link_map, cluster_links_batch: ChunkedBatchSaver) -> None:
        self.session = session
        self._link_map = link_map
        self._next_link = defaultdict(deque)
        self._cluster_links_batch = cluster_links_batch

        super().__init__(self, ClusterModelClass=KokkaiCluster)

    def save(self, datas: Iterable[tuple[ndarray, SentimentResult, Iterable[str], DTO]], model: NodeModel):
        super().save(datas, model)

        self._link_map.update(self._next_link)
        return self._link_map()

    def _get_cluster_model(self, taged, cluster_id, cluster_members):
        cluster_model = super()._get_cluster_model(taged, cluster_id, cluster_members)
        cluster_model.session = self.session
        return cluster_model

    def _put_cluster_data(self, entities, members_chunk, cluster_keyword_chunk, index2id, linked_counts_map, member_model_chunk: ChunkedBatchSaver, index2published, taged, keyword_model_chunk: ChunkedBatchSaver, member_positions_chunk: deque):
        super()._put_cluster_data(entities, members_chunk, cluster_keyword_chunk, index2id, linked_counts_map,
                                  member_model_chunk, index2published, taged, keyword_model_chunk, member_positions_chunk)
        for entity, keywords in zip(entities, members_chunk):
            eid = entity.id
            self._next_link[keywords].append((self.session, eid,))
            if keywords in self._link_map:

                for session, cluster_id in self._link_map[keywords]:
                    link_model = ClusterLink()
                    if session > self.session:
                        link_model.from_cluster = eid
                        link_model.to_cluster = cluster_id
                    else:
                        link_model.to_cluster = eid
                        link_model.from_cluster = cluster_id
                    self._cluster_links_batch.put(link_model, False)
