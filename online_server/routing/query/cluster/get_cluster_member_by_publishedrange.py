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
    q1.add_filter("count_published" ">=", start)
    q1.add_filter("count_published" "<", mid)

    q1.projection = ["text_id"]
    q1.order = ["published"]
    q2 = ClusterMember.query()
    q2.add_filter("cluster_id", "=", cluster_id)
    q2.add_filter("count_published" ">=", mid)
    q2.add_filter("count_published" "<=", end)

    q2.projection = ["text_id"]
    q2.order = ["-published"]
    itr1 = q1.fetch(limit=limit)
    itr2 = q2.fetch(limit=limit)
    return Node.get_multi([e["text_id"] for e in chain.from_iterable([itr1, itr2])])
