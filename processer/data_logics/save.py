

from hashlib import md5


import numpy as np

import logging
from db import cluster, cluster_member
from multiprocessing import Pool
from collections import deque, defaultdict


from typing import Dict, Iterable
from data_logics.node_logic import NodeLogic
from data_logics import author_keyword
from data_logics import cluster_link
from ridgedetect.taged import Taged
from doc2vec.base.doc2vec import Doc2Vec
from doc2vec.base.protocol.sentiment import SentimentResult

from db.util.chunked_batch_saver import ChunkedBatchSaver


from data_loader.dto import DTO
from cluster.get_position import get_position


def buildModel():
    return NodeLogic()


def buildVectaizer():
    return Doc2Vec()


class Logic:
    def __init__(self, ClusterModelClass=cluster.Cluster, AutherKeywordSaverClass=author_keyword.Saver) -> None:
        self._cluster_model_class = ClusterModelClass
        self._author_keyword_saver_class = AutherKeywordSaverClass
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
        innerid2clusterid = {}

        node_index = 0

        is_first = True
        logging.info('start saving')
        vector_dtype = None
        vector_dimention = None
        index2data = {}
        is_data_exist = False

        for vector, sentimentResult, keywords, data in datas:
            is_data_exist = True
            if vector is None or len(keywords) == 0:
                continue
            if is_first == True:
                is_first = False
                vector_dimention = vector.shape[0]
                vector_dtype = vector.dtype
            index2vector[node_index] = vector
            index2sentiments[node_index] = sentimentResult

            index2id[node_index] = data.id
            index2tag[node_index] = keywords
            index2published[node_index] = data.published
            index2data[node_index] = data
            node_index += 1
        if is_data_exist == False:
            logging.info('no data')
            return
        logging.info('create vectors')
        vectors = np.fromiter((index2vector[i] for i in range(node_index)), dtype=np.dtype(
            (vector_dtype, vector_dimention,)), count=node_index)

        taged = Taged()

        taged.fit(tags_map=index2tag, vectors=vectors, sample=32)
        logging.info('fit done')

        # edge_chunk = Chunker()
        linked_counts_map = defaultdict(int)
        link_counts_map = {}
        for node_index, link_node_indexs in taged.graph.items():

            link_counts_map[node_index] = len(link_node_indexs)
            for link_node_index in link_node_indexs:
                link_node_id = index2id[link_node_index]
                linked_counts_map[link_node_id] += 1

        is_apex_flag_map = {}
        for node_index, link_node_indexs in taged.graph.items():
            nodeid = index2id[node_index]
            link_count = link_counts_map[node_index]
            linked_count = linked_counts_map[nodeid]
            is_apex_flag = False

            for link_node_index in link_node_indexs:

                graph: np.ndarray = taged.graph.get(
                    link_node_index, np.array([])) == node_index
                if graph.sum() >= 1:
                    is_apex_flag = True
                    break

            is_apex_flag_map[nodeid] = is_apex_flag
        cluster_chunker = ChunkedBatchSaver()
        members_chunk = deque()

        member_model_chunk = ChunkedBatchSaver()

        # keyword_chunk = ChunkedBatchSaver()
        author_keyword_saver = self._author_keyword_saver_class()
        index2weight = {}

        logging.info('start text save')

        for node_index, nodeid in index2id.items():
            vector = index2vector[node_index]
            data = index2data[node_index]
            keywords = index2tag[node_index]
            sentimentResult = index2sentiments[node_index]

            link_node_id = [index2id[to_index]
                            for to_index in taged.graph[node_index]]
            linked_count = linked_counts_map[nodeid]
            is_apex_flag = is_apex_flag_map[nodeid]
            result, weight, published_list = nodeLogic.save(id=nodeid, dto=data, vector=vector, sentiment_result=sentimentResult,
                                                            link_to=link_node_id, linked_count=linked_count, keywords=keywords, is_apex_flag=is_apex_flag)

            index2weight[node_index] = weight
            author_keyword_saver.put(data.author_id, keywords=keywords)

            """
            現状最大5つまでなので、そのまま格納する方式に
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
        # keyword_chunk.close()

        cluster_keyword_chunk = deque()
        member_positions_chunk = deque()
        keyword_model_chunk = ChunkedBatchSaver()
        logging.info('start cluster save')
        for innerid, cluster_members in taged.clusters.items():

            positions = get_position(
                index2sentiments=index2sentiments, cluster_members=cluster_members)
            member_positions_chunk.append(positions)

            cluster_model = self._get_cluster_model(
                innerid=innerid, taged=taged, cluster_members=cluster_members, weight_map=index2weight, index2id=index2id)
            innerid2clusterid[innerid] = cluster_model.get_id()
            entities = cluster_chunker.put(cluster_model)
            cluster_keyword_chunk.append(taged.tag_index[innerid])
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

        cluster_link_saver = cluster_link.Saver()
        cluster_link_saver.put(
            taged.cluster_link, innerid2clusterid=innerid2clusterid)
        cluster_link_saver.close()
        member_model_chunk.close()
        keyword_model_chunk.close()

        logging.info('done')

    def _get_cluster_model(self, taged, innerid, cluster_members, weight_map: Dict, index2id: Dict):

        modelid = md5('//'.join(set([index2id[index] for index in cluster_members])
                                ).encode('utf-8')).hexdigest()
        cluster_model = self._cluster_model_class(id=modelid)

        cluster_model.member_count = len(cluster_members)
        cluster_model.keywords = list(
            taged.tag_index[innerid])[:5]
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
                member_model.cluster_id = entity.key.id_or_name
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
        # print(loop_count)


def process(loader, logicBuilder=Logic):
    vectaizer = buildVectaizer()
    model = buildModel()

    datas = loader('')
    logic = logicBuilder()

    vectors = vectaizer.exec(datas)

    return logic.save(vectors, model=model)
