from data_logics.kokkai_save import KokkaiLogic, KokkaiNodeLogic
from doc2vec import Doc2Vec
from doc2vec.sentiment.oseti_analizer import OsetiAnalizer
from doc2vec.tokenaizer.japanese_language.tokenaizer.mecab_tokenaizer import MeCabTokenazier
from doc2vec.indexer.japanese_language.indexer import JapaneseLanguageIndexer
from data_loader import kokkai
from db.util.chunked_batch_saver import ChunkedBatchSaver
from multiprocessing.pool import Pool
from metadata import LOCATION, PROJECT_ID
from storage import basic as storage
storage.set_location(LOCATION)
storage.set_project_id(PROJECT_ID)


def execute(loader=kokkai, LogicClass=KokkaiLogic, NodeLogicClass=KokkaiNodeLogic, Doc2VecClass=Doc2Vec, AnalizerClass=OsetiAnalizer, TokenaizerClass=MeCabTokenazier, IndexerClass=JapaneseLanguageIndexer):

    d2v = Doc2VecClass(
        is_use_title=False,
        chunksize=5,
        TokenaizerClass=TokenaizerClass,
        AnalizerClass=AnalizerClass,
        IndexerClass=IndexerClass)
    clusterLinkSaver = ChunkedBatchSaver()
    link_map = {}
    with Pool() as pool:
        for session, dtos in loader.load():
            logic = LogicClass(link_map=link_map, session=session,
                               cluster_links_batch=clusterLinkSaver)

            datas = d2v.exec(pool, dtos)

            nodeLogic = NodeLogicClass(session=session)
            link_map, nodeModel = logic.save(datas, nodeLogic=nodeLogic)
            meeting_keywords = nodeModel.get_meeting_keywords()
            loader.save_meeting(meeting_keywords)
        clusterLinkSaver.close()
        loader.close_meeting_saver()
