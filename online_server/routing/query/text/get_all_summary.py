from online_server.db.node import Node
import itertools


def fetch(limit: int = 200):
    q = Node.query()
    q.order = ['-weight']

    return q.fetch(limit=limit)
