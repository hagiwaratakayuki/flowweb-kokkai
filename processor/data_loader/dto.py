from datetime import datetime
from typing import Any


class DTO:
    _is_use_title: bool = True
    _line_break: str = r'\n'

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

    def get_text(self) -> str:
        if self._is_use_title == True:
            return self.title + self._line_break + self.body
        else:
            return self.body
