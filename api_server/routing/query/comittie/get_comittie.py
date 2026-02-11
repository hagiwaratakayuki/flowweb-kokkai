import asyncio
from db.kokkai_comittie import KokkaiComittie
from routing.entity_types.kokkai_comittie import KokkaiComittie as KokkaiComittieEntity


async def fetch(comittie_id) -> KokkaiComittieEntity:
    return await KokkaiComittie.get_async(id=comittie_id)
