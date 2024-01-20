

# from file_reader.newsgroup import load
import numpy as np
from db import cluster, cluster_member, model as db_model
from multiprocessing import Pool
import multiprocessing as multi
from db import edge
from processer.db import node
from ridgedetect.taged import Taged


def process():
    vectaizer = buildVectaizer()
    model = buildModel()
    return _process(loader=load, model=model, vectaizer=vectaizer)


class Model:

    def __init__(self) -> None:
        self._chunk = []
        self._vectotrs = []
        self._keywords = []

    def save(self, data, vector, sentimentresult, keyword):
        textEntity = node.Node()
        textEntity.setProperty('',  data.article, dict(
            vector=vector, sentiment=sentimentresult))
        self._vectotrs.append(vector)
        self._keywords.append(keyword)

        self._chunk.append(textEntity)
        self._vectotrs.append(vector)
        if len(self._chunk) < 30:
            return
        entities = db_model.put_multi(self._chunk)
        ret = zip(self._vectotrs, self._keywords, entities)

        self._chunk = []
        self._vectotrs = []
        self._keywords = []

        return ret

    def finish(self):
        entities = db_model.put_multi(self._chunk)
        self._chunk = []
        return entities


def buildModel():
    return Model()


def buildVectaizer():
    pass

# ファイルを読む
# パース
# クラスタリング　+ キーワード抽出
# 保存


def _process(loader, model: Model, vectaizer, workers=multi.cpu_count()):
    datas = loader()
    tags_map = {}
    index2id = {}

    vectors_map = {}
    index = 0

    shape = [0, 0]
    is_first = True
    for vector, sentimentResults, keywords, data in vectaizer.exec(datas):
        result = model.save(data, vector, sentimentResults, keywords)
        if result == None:
            continue

        for vec, keywords, entity in result:
            if is_first == True:
                is_first = False
                shape[1] = vec.shape[1]
            vectors_map[index] = vec
            index2id[index] = entity.id
            vectors_map[index] = vec
            tags_map[index] = keywords
            index += 1

    result = model.finish()

    for vec, keywords, entity in result:
        if is_first == True:
            is_first = False
            shape[1] = vec.shape[1]
        vectors_map[index] = vec
        index2id[index] = entity.id
        vectors_map[index] = vec
        tags_map[index] = keywords
        index += 1
    shape[0] = index

    vectors = np.zeros(shape=shape)
    for i, v in vectors_map.items():
        vectors[i] = v
    taged = Taged()
    taged.fit(tags_map=tags_map, vectors=vectors, sample=32)
    count = 0
    chunk = []
    members_chunk = []
    connect_count_cache = {}
    member_model_chunk = []
    member_model_count = 0
    for cluster_members in taged.clusters.values():
        cluster_model = cluster.Cluster()
        cluster_model.member_count = len(cluster_members)
        chunk.append(cluster_model)
        members_chunk.append(cluster_members.values())
        count += 1
        if count >= 30:

            entities = db_model.put_multi(chunk)
            for entity, members in zip(entities, members_chunk):
                for member in members:
                    member_model = cluster_member.ClusterMember()
                    member_model.cluster = entity.id
                    member_model.text = index2id[member]
                    if not member in connect_count_cache:
                        connect_count_cache[member] = len(
                            taged.graph.get(member, {}))
                    member_model.connect = connect_count_cache[member]
                    member_model_chunk.append(member_model)
                    member_model_count += 1
                    if member_model_count >= 30:
                        db_model.put_multi(member_model_chunk)
                        member_model_count = 0
    if count > 0:
        entities = db_model.put_multi(chunk)
        for entity, members in zip(entities, members_chunk):
            for member in members:
                member_model = cluster_member.ClusterMember()
                member_model.cluster = entity.id
                member_model.text = index2id[member]
                if not member in connect_count_cache:
                    connect_count_cache[member] = len(
                        taged.graph.get(member, {}))
                member_model.connect = connect_count_cache[member]
                member_model_chunk.append(member_model)
                member_model_count += 1
                if member_model_count >= 30:
                    db_model.put_multi(member_model_chunk)
                    member_model_count = 0
    if member_model_count > 0:
        db_model.put_multi(member_model_chunk)
    chunk = []
    count = 0
    for ind, vertexs in taged.graph.items():
        for vertex in vertexs:
            model_entity = edge.Edge()
            model_entity.linked_from = index2id[ind]
            model_entity.link_to = index2id[vertex]
            chunk.append(model)
            count += 1
            if count >= 30:
                db_model.put_multi(chunk)
                count = 0
                chunk = []
    if count > 0:
        db_model.put_multi(chunk)
