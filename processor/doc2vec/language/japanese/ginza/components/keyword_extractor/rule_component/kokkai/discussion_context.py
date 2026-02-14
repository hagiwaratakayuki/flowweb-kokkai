from typing import Any

from data_loader.kokkai import DTO


class DiscussionContext:
    data: Any
    discussion_id: Any

    def __init__(self):
        self.data = None
        self.discussion_id = ''

    def set_data(self, data, dto: DTO):
        self.data = data
        self.discussion_id = dto.discussion_id

    def get_data(self, dto: DTO):
        if dto.discussion_id != self.discussion_id or self.data == None:
            self.discussion_id = dto.discussion_id
            self.data = None
            return False, False
        else:
            return True, self.data
