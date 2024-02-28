from .model import Model
from typing import Union, List
import json
import math
from datetime import datetime
import re
spliter = re.compile('[\s\w]+')


class Node(Model):
    data: str
    author: str = ''
    author_id: str = ''
    link_to: Union[List[str], None]
    linked_count: int
    published: datetime
    weight: float
    title: str
    published_list: List[str]
    hash: str

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", )}, *args, **kwargs)

    def setProperty(self, data, title,  link_to: list[str], linked_count: int, published: datetime, author: str, author_id: str, hash: str):
        self.link_to = link_to

        if type(published) == str:
            published = datetime.fromisoformat(published)
        self.author = author
        self.author_id = author_id
        self.published = published
        self.title = title
        self.data = json.dumps(data)
        self.linked_count = linked_count
        self.hash = hash
        datetime_list = spliter.split(str(published))
        year = datetime_list[0]
        year_month = '-'.join(datetime_list[:2])
        year_month_date = '_'.join(datetime_list[:3])
        self.published_list = [year, year_month, year_month_date]

        if linked_count == 0:
            weight = 0.0
        else:
            weight = math.log(linked_count) * (float(published.year) +
                                               float(published.month) / 100.0 + float(published.day) / 10000.0)

        self.weight = weight
