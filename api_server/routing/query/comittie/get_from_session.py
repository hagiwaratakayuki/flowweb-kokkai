
from typing import Iterable, Literal, Tuple
from routing.query.pattern import cursorfetch
from db.kokkai_comittie import KokkaiComittieAndSession
from routing.entity_types.kokkai_comittie import KokkaiComittieAndSession as KokkaiComittieAndSessionEntityType
import asyncio


async def fetch(name, session, house=None, cursor=None, limit=10) -> Tuple[Iterable[KokkaiComittieAndSessionEntityType], str | Literal[False]]:

    await asyncio.sleep(0)
    query = KokkaiComittieAndSession.query()
    query.add_filter('name', '=', name)
    if house is not None:
        query.add_filter('house', '=', house)
    if session is not None:
        query.add_filter('session', '=', session)
    return cursorfetch.fetch(query, cursor=cursor, limit=limit)


def indexer():
    asyncio.run(fetch('index', 0, 0))
    asyncio.run(fetch('index', 0))
