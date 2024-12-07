from db.model import put_multi
from collections import deque

import asyncio
import time
import math

START_LIMIT = 500
LIMIT_INCREASE_STEP = 1.5
LIMIT_INCREASE_TIME = 5.0 * 60.0
LIMIT_MAP = {}
PREV_CALL_TIMES = {}
WRITE_START_MAP = {}
MAX_LIMIT = 5000


class ChunkedBatchSaver:
    def __init__(self, size: int = 50):

        self.size = size

        self._write_start = 0
        self._write_limit = 500
        self._prev_call_time = 0.0
        self._clear_weigtings()
        self._clear_chunk()

    def put(self, model, is_return=True):
        self._chunk.append(model)
        self.chunk_count += 1
        self._model = model
        if self.chunk_count >= self.size:
            return self._put_chunk(is_return=is_return)

    def close(self, is_return=True):

        if self.chunk_count > 0:
            return self._put_chunk(is_force=True, is_return=is_return)

    def _put_chunk(self, is_force=False, is_return=True):
        global LIMIT_MAP, PREV_CALL_TIMES
        now = time.time()

        chunk = self._clear_chunk()

        # return put_multi(chunk)

        self._weightings.append(chunk)
        self._weightings_count += self.size
        write_limit = LIMIT_MAP.get(self._model.get_kind(), START_LIMIT)
        is_time_over = self._prev_call_time > 0.0 and now - self._prev_call_time > 1.0
        if is_force == False and (is_time_over == False or self._weightings_count + self.size < write_limit):
            return
        write_start = WRITE_START_MAP.get(self._model.get_kind(), 0)
        if write_start == 0:
            WRITE_START_MAP[self._model.get_kind()] = now
        else:
            LIMIT_MAP[self._model.get_kind()] = min(START_LIMIT *
                                                    LIMIT_INCREASE_STEP ** math.floor(
                                                        (now - write_start) / LIMIT_INCREASE_TIME), MAX_LIMIT)
        weightings = self._clear_weigtings()

        return asyncio.run(self._put_waitings(weightings=weightings, is_return=is_return))

    async def _put_waitings(self, weightings, is_return=True):
        now = time.time()
        from_prev_time = now - self._prev_call_time

        if from_prev_time < 1.0:

            await asyncio.sleep(from_prev_time)
            now = time.time()
        self._prev_call_time = now
        chunks = await asyncio.gather(*[self._put_multi(weight) for weight in weightings])
        if is_return == False:
            return
        ret = deque()
        for chunk in chunks:
            for entity in chunk:
                ret.append(entity)
        return ret

    def _clear_chunk(self):

        chunk = getattr(self, '_chunk', [])
        self._chunk = deque()
        self.chunk_count = 0
        return chunk

    def _clear_weigtings(self):

        weightings = getattr(self, '_weightings', [])
        self._weightings = []
        self._weightings_count = 0
        return weightings

    async def _put_multi(self, chunk):

        await asyncio.sleep(0)

        return put_multi(chunk)
