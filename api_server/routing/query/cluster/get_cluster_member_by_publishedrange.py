from db.proxy import Node
from db.proxy import ClusterMember
from datetime import datetime, timedelta
from itertools import chain
import math


def fetch(cluster_id: str,
          start_year: int,
          start_month: int,
          start_date: int,
          end_year: int,
          end_month: int,
          end_date: int,
          limit: int = 50):

    start = datetime(start_year, start_month, start_date)
    end = datetime(end_year, end_month, end_date)
    range_delta = end - start
    mid = end - range_delta / 2
    q1 = ClusterMember.query()

    q1.add_filter("cluster_id", "=", cluster_id)
    q1.add_filter("published", ">=", start)
    q1.add_filter("published", "<=", end)

    q1.projection = ["node_id"]
    q1.order = ["-published"]
    itr1 = q1.fetch(limit=limit)

    return Node.get_multi([e["node_id"] for e in itr1])


def indexer():
    fetch(0, 1, 1, 1, 1, 1, 1)
