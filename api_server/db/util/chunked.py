from db.model import put_multi
from collections import deque
class Chunker:
    def __init__(self, limit:int=30):
        self.chunk = deque()
        self.chunk_count = 0
        self.limit = limit
    def put(self, model):
        self.chunk.append(model)
        self.chunk_count += 1
        if self.chunk_count >= self.limit:
            ret = put_multi(self.chunk)
            self.chunk = deque()
            self.chunk_count = 0
            return ret
    def close(self):
        if self.chunk_count > 0:
            return put_multi(self.chunk)
        




    