from datetime import datetime
from typing import Any


class DTO:
    def __init__(self,
                 title: str = '',
                 id: Any = '',
                 body: Any = '',
                 author: Any = '',
                 author_id: Any = '',
                 published: Any = None,
                 data: Any = {}):
        self.title = title
        self.id = id
        self.body = body
        self.data = data.copy()
        self.published = published
        self.author = author
        self.author_id = author_id
