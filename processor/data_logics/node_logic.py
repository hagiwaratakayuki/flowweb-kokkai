from data_loader.dto import DTO
from db import node, node_body
from db.util.chunked_batch_saver import ChunkedBatchSaver
from doc2vec.base.protocol.sentiment import SentimentResult
import datetime
import json
import math
import re
import numpy as np
from contract_logics.node import get_hash, get_ymd, NodeData, SentimentData
from utillib import hash
spliter = re.compile(r'[\s\w]+')


class NodeLogic(ChunkedBatchSaver):
    def __init__(self, NodeModel: node.Node = node.Node, NodeBodyModel=node_body.NodeBody, NodBodySaverClass: ChunkedBatchSaver = ChunkedBatchSaver, size: int = 30):
        super().__init__(size)
        self.nodeModel = NodeModel
        self.nodeBodyModel = NodeBodyModel
        self.nodeBodySaver = NodBodySaverClass(size)

    def save(self, id, dto: DTO, vector, sentiment_result: SentimentResult, link_to: list[str], linked_count: int, keywords: list[str], is_apex_flag: bool):

        nodeEntity = self.nodeModel(id=id)

        nodeBodyEntity = self.nodeBodyModel(id=id)
        nodeBodyEntity.body = dto.body
        self.nodeBodySaver.put(nodeBodyEntity)
        sentiment = self.set_vectors(sentiment_result=sentiment_result)
        weight, publishedlist = self.setEntityProperty(
            entity=nodeEntity,
            dto=dto,
            nodeEntity=nodeEntity,
            vector=vector,
            link_to=link_to,
            linked_count=linked_count,
            sentiment=sentiment,
            keywords=keywords,
            is_apex_flag=is_apex_flag)

        return self.put(nodeEntity), weight, publishedlist

    def set_vectors(self, sentiment_result: SentimentResult):
        direction_vector = sentiment_result.vectors.positive - \
            sentiment_result.vectors.negative

        if sum(direction_vector) == 0:
            direction_vector = sentiment_result.vectors.neutral

        sentiment: SentimentData = {
            'position': sentiment_result.vectors.neutral.tolist(),
            'direction': direction_vector.tolist()
        }
        return sentiment

    def setEntityProperty(self, entity: node.Node, dto: DTO, nodeEntity: node.Node, vector: np.ndarray, link_to, linked_count, sentiment, keywords, is_apex_flag):

        data: NodeData = dict(vector=vector.tolist(),
                              sentiment=sentiment)
        title = dto.title
        link_to = link_to
        linked_count = linked_count
        published = dto.published
        author = dto.author
        author_id = dto.author_id

        entity.link_to = link_to

        if type(published) == str:
            published = datetime.datetime.fromisoformat(published)

        entity.author = author
        entity.author_id = author_id
        entity.published = published
        entity.title = title
        entity.data = json.dumps(data)
        entity.linked_count = linked_count
        entity.hash = get_hash(vector=vector)
        entity.keywords = keywords
        entity.is_apex = is_apex_flag
        datetime_list = spliter.split(str(published))

        entity.published_list = get_ymd(datetime_list)

        if linked_count == 0:
            weight = 0.0
        else:
            weight = math.log(linked_count) * (float(published.year) +
                                               float(published.month) / 100.0 + float(published.day) / 10000.0)

        entity.weight = weight

        return weight, entity.published_list

    def close(self, is_return=True):
        res = super().close(is_return)

        self.nodeBodySaver.close()
        if is_return == True:
            return res
