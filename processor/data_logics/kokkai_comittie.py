import json
from math import inf
from operator import itemgetter


from db.util.chunked_batch_saver import ChunkedBatchSaver
from typing import Any, Dict, Tuple, TypedDict
from db.kokkai_comittie import KokkaiComittie, KokkaiComittieAndSession
from contract_logics.kokkai_comittie import start_end, get_supersets

import re

from data_logics import kokkai_comittie
from db import meeting
number_pt = re.compile(r'\d+')


class ComittieData:
    start: int = inf
    end: int = 0


class SessionComittieDataType(TypedDict):
    max_issue: int
    meetings: list[Tuple[int, str]]


issue_getter = itemgetter(0)
meeting_getter = itemgetter(1)

ComittieMapType = Dict[str, kokkai_comittie.ComittieData]


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, comittie_map: ComittieMapType):
        for name, data in comittie_map.items():
            entity = KokkaiComittie()
            entity.name = name
            entity.start = int(data.start)
            entity.end = data.end
            entity.start_end = start_end(data.start, data.end)

            entity.supersets = get_supersets(name=name) or []
            self.saver.put(entity)

    def close(self):
        self.saver.close()


class SessionSaver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, session, session_comittie_data_map: Dict[str, Dict[str, SessionComittieDataType]]):
        for name, house_and_datas in session_comittie_data_map.items():
            for house, data in house_and_datas.items():

                entity = KokkaiComittieAndSession()

                entity.house = house
                entity.issue_count = data['max_issue']
                entity.name = name
                entity.session = session
                entity.meeting_ids = json.dumps([meeting_getter(meeting) for meeting in sorted(
                    data['meetings'], key=issue_getter)])
                self.saver.put(entity)

    def _reguraise(self, row):
        if isinstance(row, str):
            match = number_pt.search(row)
            if not match:
                return None
            return int(match.group(0))

    def close(self):
        self.saver.close()
