from db.proxy import Node
from typing import Optional, Union


def fetch(node_id: Union[str, int], cursor: Optional[str] = None, limit: int = 10):
    start_cursor = None
    if cursor != None:
        start_cursor = cursor.encode('utf-8')
    query = Node.query()
    query.add_filter('link_to', '=', node_id)
    query.order = ["linked_count"]
    itr = query.fetch(start_cursor=start_cursor, limit=limit)
    next_page_token = False
    if itr.next_page_token != None:
        next_page_token = itr.next_page_token.decode('utf-8')
    return itr, next_page_token
