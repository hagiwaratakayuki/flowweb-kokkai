from .get_from_session import fetch


async def comittie():
    await fetch(house='test', session=1)
