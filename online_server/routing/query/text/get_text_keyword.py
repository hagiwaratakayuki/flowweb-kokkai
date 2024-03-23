from db.proxy import NodeKeyword


def fetch(text_id: str | int):
    query = NodeKeyword.query()
    query.add_filter("text_id", "=", text_id)
    query.projection = ["keyword"]
    return [e["keyword"] for e in query.fetch()]
