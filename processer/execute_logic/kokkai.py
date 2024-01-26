from data_logics.kokkai_save import KokkaiLogic, KokkaiNodeModel
from doc2vec import Doc2Vec
from doc2vec.sentiment.oseti_analizer import OsetiAnalizer
from doc2vec.tokenaizer.mecab_tokenaizer import MeCabTokenazier
from data_loader import kokkai
from db.util.chunked_batch_saver import ChunkedBatchSaver


def execute(loader=kokkai.load, LogicClass=KokkaiLogic, ModelClass=KokkaiNodeModel, Doc2VecClass=Doc2Vec, AnalizerClass=OsetiAnalizer, TokenaizerClass=MeCabTokenazier):

    d2v = Doc2VecClass(
        chunksize=50, TokenaizerClass=TokenaizerClass, AnalizerClass=AnalizerClass)
    clusterLinkSaver = ChunkedBatchSaver()
    link_map = {}
    for session, datas in loader():
        logic = LogicClass(link_map=link_map, session=session,
                           cluster_links_batch=clusterLinkSaver)
        model = ModelClass(session=session)
        vectors = d2v.exec(datas)

        link_map = logic.save(vectors, model=model)
    clusterLinkSaver.close()

    return
