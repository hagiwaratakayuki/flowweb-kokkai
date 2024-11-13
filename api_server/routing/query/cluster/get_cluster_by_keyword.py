from db.proxy import Cluster
from ..pattern import cursorfetch


def fetch(keyword: str, limit=10):
    query = Cluster.query()
    query.add_filter("keyword", "=", keyword)

    return query.fetch()
