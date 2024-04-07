from tkinter import NO
from typing import Iterable
from db.kokkai_comittie import KokkaiComittieAndSession
from routing.entity_types.kokkai_comittie import KokkaiComittieAndSession as KokkaiComittieAndSessionEntity
import asyncio


async def fetch(house=None, session=None) -> Iterable[KokkaiComittieAndSessionEntity]:
    if house is None and session is None:
        raise Exception()
    await asyncio.sleep(0)
    query = KokkaiComittieAndSession.query()
    if house is not None:
        query.add_filter('house', '=', house)
    if session is not None:
        query.filters('session', '=', session)
    return query.fetch()
