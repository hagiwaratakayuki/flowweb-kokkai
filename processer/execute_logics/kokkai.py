from data_logics.kokkai_save import KokkaiLogic, KokkaiNodeLogic
from doc2vec import Doc2Vec
from doc2vec.sentiment.oseti_analizer import OsetiAnalizer
from doc2vec.tokenaizer.mecab_tokenaizer import MeCabTokenazier
from doc2vec.indexer.japanes_language import JapaneseLanguageIndexer
from data_loader import kokkai
from db.util.chunked_batch_saver import ChunkedBatchSaver
from multiprocessing.pool import Pool


def execute(loader=kokkai.load, LogicClass=KokkaiLogic, NodeLogicClass=KokkaiNodeLogic, Doc2VecClass=Doc2Vec, AnalizerClass=OsetiAnalizer, TokenaizerClass=MeCabTokenazier, IndexerClass=JapaneseLanguageIndexer):

    d2v = Doc2VecClass(
        is_use_title=False,
        chunksize=50,
        TokenaizerClass=TokenaizerClass,
        AnalizerClass=AnalizerClass,
        IndexerClass=IndexerClass)
    clusterLinkSaver = ChunkedBatchSaver()
    link_map = {}
    with Pool() as pool:
        for session, datas in loader():
            logic = LogicClass(link_map=link_map, session=session,
                               cluster_links_batch=clusterLinkSaver)

            datas = d2v.exec(pool, datas)
            nodeLogic = NodeLogicClass(session=session)
            link_map = logic.save(datas, nodeLogic=nodeLogic)
        clusterLinkSaver.close()

    return