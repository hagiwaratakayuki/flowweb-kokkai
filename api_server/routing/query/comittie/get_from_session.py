from db.kokkai_comittie import KokkaiComittieAndSession
from routing.entity_types.kokkai_comittie import KokkaiComittieAndSession as KokkaiComittieAndSessionEntity
import asyncio


async def fetch(house=None, session=None) -> KokkaiComittieAndSessionEntity:
    await asyncio.sleep(0)
    query = KokkaiComittieAndSession.query()

    return
