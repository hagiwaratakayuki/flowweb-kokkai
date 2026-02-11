from typing import Iterable
from db.kokkai_comittie import KokkaiComittie
from routing.entity_types.kokkai_comittie import KokkaiComittie as KokkaiComittieEntity
import asyncio


async def fetch() -> Iterable[KokkaiComittieEntity]:
    await asyncio.sleep(0)
    return KokkaiComittie.query().fetch()
