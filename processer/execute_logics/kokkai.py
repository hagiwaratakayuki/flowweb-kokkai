from data_logics.kokkai_save import KokkaiLogic, KokkaiNodeLogic


from data_loader import kokkai
from db.util.chunked_batch_saver import ChunkedBatchSaver

from metadata import LOCATION, PROJECT_ID
from doc2vec.spacy.japanese_language.doc2vec.kokkai import builder as doc2vec_builder
from doc2vec.base.doc2vec import Doc2Vec
from storage import basic as storage
storage.set_location(LOCATION)
storage.set_project_id(PROJECT_ID)


def execute(loader=kokkai, LogicClass=KokkaiLogic, NodeLogicClass=KokkaiNodeLogic, Doc2VecClass=doc2vec_builder):

    d2v: Doc2Vec = Doc2VecClass()
    clusterLinkSaver = ChunkedBatchSaver()
    link_map = {}

    for session, dtos in loader.load():
        logic = LogicClass(link_map=link_map, session=session,
                           cluster_links_batch=clusterLinkSaver)

        datas = d2v.exec(dtos)

        nodeLogic = NodeLogicClass(session=session)
        link_map, nodeModel = logic.save(datas, nodeLogic=nodeLogic)
        meeting_keywords = nodeModel.get_meeting_keywords()
        loader.save_meeting(meeting_keywords)
    clusterLinkSaver.close()
    loader.close_meeting_saver()
