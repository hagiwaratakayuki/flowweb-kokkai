from .model import Model
from typing import Optional, Union, List
from datetime import datetime


class Node(Model):
    data: str
    author: str = ''
    author_id: str = ''
    link_to: Union[List[str], None]
    linked_count: int
    published: datetime
    weight: float
    title: str
    published_list: Optional[List[str]]
    keywords: List[str]
    is_apex: bool
    hash: str

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", "author",)}, *args, **kwargs)
