
from functools import reduce
import numpy as np
import logging
from db import cluster, cluster_member
from multiprocessing import Pool
from collections import deque, defaultdict
from db import node_keyword

from typing import Dict, Iterable
from data_logics.node_logic import NodeLogic
from ridgedetect.taged import Taged
from doc2vec import Doc2Vec
from doc2vec.indexer.dto import SentimentResult

from db.util.chunked_batch_saver import ChunkedBatchSaver


from data_loader.dto import DTO
from cluster.get_position import get_position


def buildModel():
    return NodeLogic()


def buildVectaizer():
    return Doc2Vec()


class Logic:
    def __init__(self, ClusterModelClass=cluster.Cluster) -> None:
        self._cluster_model_class = ClusterModelClass
    # ファイルを読む
    # パース
    # クラスタリング　+ キーワード抽出
    # 保存

    def save(self, datas: Iterable[tuple[np.ndarray, SentimentResult, Iterable[str], DTO]], nodeLogic: NodeLogic):

        index2tag = {}
        index2id = {}
        index2published = {}
        index2sentiments: dict[int, SentimentResult] = {}

        index2vector = {}

        index = 0

        is_first = True
        logging.info('start saving')
        vector_dtype = None
        vector_dimention = None
        index2data = {}

        for vector, sentimentResult, keywords, data in datas:

            if vector is None:
                continue
            if is_first == True:
                is_first = False
                vector_dimention = vector.shape[0]
                vector_dtype = vector.dtype
            index2vector[index] = vector
            index2sentiments[index] = sentimentResult

            index2id[index] = data.id
            index2tag[index] = keywords
            index2published[index] = data.published
            index2data[index] = data
            index += 1

        logging.info('create vectors')
        vectors = np.fromiter((index2vector[i] for i in range(index)), dtype=np.dtype(
            (vector_dtype, vector_dimention,)), count=index)

        taged = Taged()

        taged.fit(tags_map=index2tag, vectors=vectors, sample=32)
        logging.info('fit done')

        # edge_chunk = Chunker()
        linked_counts_map = defaultdict(int)
        for vertexs in taged.graph.values():
            for vertex in vertexs:
                link_to = index2id[vertex]
                linked_counts_map[link_to] += 1

        cluster_chunker = ChunkedBatchSaver()
        members_chunk = deque()

        member_model_chunk = ChunkedBatchSaver()

        keyword_chunk = ChunkedBatchSaver()
        index2weight = {}

        logging.info('start text save')

        for index, id in index2id.items():
            vector = index2vector[index]
            data = index2data[index]
            keywords = index2tag[index]

            link_to = [index2id[to_index] for to_index in taged.graph[index]]
            linked_count = linked_counts_map[id]
            result, weight, published_list = nodeLogic.save(id=id, dto=data, vector=vector, sentiment_result=sentimentResult,
                                                            link_to=link_to, linked_count=linked_count, keywords=keywords)

            index2weight[index] = weight
            """
            for keyword in keywords:
                keyword_model = node_keyword.NodeKeyword()
                keyword_model.published = data.published
                keyword_model.weight = weight
                keyword_model.published_list = published_list
                keyword_model.linked_count = linked_count
                keyword_model.keyword = keyword
                keyword_model.node_id = id
                keyword_chunk.put(keyword_model)
            """

        entities = nodeLogic.close()
        keyword_chunk.close()

        cluster_keyword_chunk = deque()
        member_positions_chunk = deque()
        keyword_model_chunk = ChunkedBatchSaver()
        logging.info('start cluster save')
        for cluster_id, cluster_members in taged.clusters.items():
            positions = get_position(
                index2sentiments=index2sentiments, cluster_members=cluster_members)
            member_positions_chunk.append(positions)

            cluster_model = self._get_cluster_model(
                cluster_id=cluster_id, taged=taged,  cluster_members=cluster_members, weight_map=index2weight)
            entities = cluster_chunker.put(cluster_model)
            cluster_keyword_chunk.append(taged.tag_index[cluster_id])
            members_chunk.append(cluster_members)

            if entities != None:
                logging.info('start cluster data save')

                self._put_cluster_data(
                    entities=entities,
                    members_chunk=members_chunk,
                    cluster_keyword_chunk=cluster_keyword_chunk,
                    index2id=index2id,
                    linked_counts_map=linked_counts_map,
                    member_model_chunk=member_model_chunk,
                    index2published=index2published,
                    taged=taged,
                    keyword_model_chunk=keyword_model_chunk,
                    member_positions_chunk=member_positions_chunk,
                    weight_map=index2weight
                )
                members_chunk = deque()
                cluster_keyword_chunk = deque()
                member_positions_chunk = deque()

        entities = cluster_chunker.close()
        if entities != None:
            logging.info('start cluster data save')
            self._put_cluster_data(
                entities=entities,
                members_chunk=members_chunk,
                cluster_keyword_chunk=cluster_keyword_chunk,
                index2id=index2id,
                linked_counts_map=linked_counts_map,
                member_model_chunk=member_model_chunk,
                index2published=index2published,
                taged=taged,
                keyword_model_chunk=keyword_model_chunk,
                member_positions_chunk=member_positions_chunk,
                weight_map=index2weight
            )

        member_model_chunk.close()
        keyword_model_chunk.close()

        logging.info('done')

    def _get_cluster_model(self, taged, cluster_id, cluster_members, weight_map: Dict):
        cluster_model = self._cluster_model_class()

        cluster_model.member_count = len(cluster_members)
        cluster_model.keywords = list(
            taged.tag_index[cluster_id])[:5]
        total_weight = 0.0
        member_count = 0
        for member in cluster_members:
            total_weight += weight_map[member]
            member_count += 1

        cluster_model.weight = total_weight / member_count
        return cluster_model

    def _put_cluster_data(
            self,
            entities,
            members_chunk,
            cluster_keyword_chunk,
            index2id,
            linked_counts_map,
            member_model_chunk: ChunkedBatchSaver,
            index2published,
            taged,
            keyword_model_chunk: ChunkedBatchSaver,
            member_positions_chunk: deque,
            weight_map: Dict

    ):
        loop_count = 0
        for entity, members, keywords, positions in zip(entities, members_chunk, cluster_keyword_chunk, member_positions_chunk):

            for member, position in zip(members, positions):
                loop_count += 1
                member_model = cluster_member.ClusterMember()
                member_model.cluster_id = entity.id
                member_model.node_id = index2id[member]
                linked_count = linked_counts_map[member]
                published = index2published[member]
                member_model.linked_count = linked_count
                member_model.published = published
                member_model.position = position
                member_model.weight = weight_map[member]

                member_model_chunk.put(member_model)

            # Temporary off
            """"
            for keyword in keywords:
                loop_count += 1
                keyword_model = cluster_keyword.ClusterKeyword()
                keyword_model.keyword = keyword
                keyword_model.cluster_id = entity.id
                keyword_model_chunk.put(keyword_model)
            """


def process(loader, logicBuilder=Logic):
    vectaizer = buildVectaizer()
    model = buildModel()

    datas = loader('')
    logic = logicBuilder()

    vectors = vectaizer.exec(datas)

    return logic.save(vectors, model=model)
