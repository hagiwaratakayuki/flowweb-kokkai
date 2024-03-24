from db.proxy import NodeKeyword
from typing import Union


def fetch(text_id: Union[str, int]):
    query = NodeKeyword.query()
    query.add_filter("text_id", "=", text_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
