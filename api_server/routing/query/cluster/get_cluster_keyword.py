from db.proxy import ClusterKeyword


def fetch(cluster_id: int):
    query = ClusterKeyword.query()
    query.add_filter("cluster_id", "=", cluster_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
