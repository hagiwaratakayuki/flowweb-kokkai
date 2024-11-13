
from typing import Optional

from google.cloud.datastore.query import Query


def fetch(query: Query, cursor: Optional[str] = None, limit: int = 10):
    start_cursor = None

    if (not cursor) is False:
        start_cursor = cursor.encode('utf-8')
    itr = query.fetch(start_cursor=start_cursor, limit=limit)
    next_page_token = False
    if itr.next_page_token != None:
        next_page_token = itr.next_page_token.decode('utf-8')

    return itr, next_page_token
