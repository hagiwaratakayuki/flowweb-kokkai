
from hashlib import md5
from os import link
from typing import Any, DefaultDict, Deque, Dict, Tuple
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.cluster_link import ClusterLink


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def put(self, cluster_links: DefaultDict[Any, Dict[Any, Any]], innerid2clusterid):
        for start_index, links in cluster_links.items():
            link_start = innerid2clusterid[start_index]
            for target_index, link_count in links.items():
                link_target = innerid2clusterid[target_index]
                model = ClusterLink(
                    id=md5('_'.join((link_start, link_target,)).encode()).hexdigest())
                model.link_start = link_start
                model.link_target = link_target
                model.link_count = link_count
                self.saver.put(model=model)

    def close(self):
        self.saver.close()
