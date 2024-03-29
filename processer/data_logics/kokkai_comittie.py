from math import inf

from more_itertools import tail
from db.util.chunked_batch_saver import ChunkedBatchSaver
from typing import Any, Dict
from db.kokkai_comittie import KokkaiComittie, KokkaiComittieAndSession
from contract_logics.kokkai_comittie import start_end, name_escape, get_supersets

import re

from data_logics import kokkai_comittie
number_pt = re.compile('\d+')


class ComittieData():
    start: int = inf
    end: int = 0


ComittieMapType = Dict[str, kokkai_comittie.ComittieData]


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, comittie_map: ComittieMapType):
        for name, data in comittie_map.items():
            entity = KokkaiComittie()
            entity.name = name
            entity.start = data.start
            entity.end = data.end
            entity.start_end = start_end(data.start, data.end)

            entity.supersets = get_supersets(name=name) or []
            self.saver.put(entity)

    def close(self):
        self.saver.close()


class SessionSaver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, session, session_comittie_data_map: Dict[str, Dict[str, list[Any]]]):
        for name, house_and_issues in session_comittie_data_map.items():
            for house, issues in house_and_issues.items():

                entity = KokkaiComittieAndSession()
                issue_count = max(map(self._reguraise, issues)) or 0
                entity.house = house
                entity.issue_count = issue_count
                entity.name = name
                entity.session = session
                self.saver.put(entity)

    def _reguraise(self, row):
        if isinstance(row, str):
            match = number_pt.search(row)
            if not match:
                return None
            return int(match.group(0))

    def close(self):
        self.saver.close()
