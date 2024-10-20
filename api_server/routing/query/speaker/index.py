from .search_speaker_by_name import fetch as search


async def speaker():
    await search('test')
