from numpy import ndarray
from processer.db.node import Node
from .save import Logic, NodeModel
from db.speech import Speech


class SpeechModel(NodeModel):
    session: int

    def setEntityProperty(self, dto, nodeEntity: Node, vector: ndarray, link_to, linked_count, sentiment):
        return super().setEntityProperty(dto, nodeEntity, vector, link_to, linked_count, sentiment)


class KokkaiLogic(Logic):
    pass
