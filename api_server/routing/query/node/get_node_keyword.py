from db.proxy import NodeKeyword
from typing import Union


def fetch(node_id: Union[str, int]):
    query = NodeKeyword.query()
    query.add_filter("node_id", "=", node_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
