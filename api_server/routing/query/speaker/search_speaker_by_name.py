from itertools import combinations
from db.speaker import Speaker
from routing.query.pattern import cursorfetch
from google.cloud.datastore.query import PropertyFilter
import asyncio


async def fetch(speaker_name, house=None, session_from=None, session_to=None, group=None, cursor=None, limit=10):
    await asyncio.sleep(0)

    query = Speaker.query()
    query.add_filter(filter=PropertyFilter('name', '>=', speaker_name))
    query.add_filter(filter=PropertyFilter('name', '<', speaker_name + '{'))
    if (not house) is False:
        query.add_filter(filter=PropertyFilter('house', '=', house))
    if (not session_from) is False:
        query.add_filter(filter=PropertyFilter('session', '>=', session_from))
    if (not session_to) is False:
        query.add_filter(filter=PropertyFilter('session', '<=', session_to))
    if (not group) is False:
        query.add_filter(filter=PropertyFilter('group', '=', group))

    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)


def indexer():
    base = {'speaker_name': 'test'}
    keys = ['group', 'session_to', 'session_from', 'house']
    """
    e = Speaker()
    e.name = 'test'
    e.house = 'test'
    e.session = 1
    e.group = 'test'

    e.upsert()
    query = Speaker.query()
    query.add_filter(filter=PropertyFilter('name', '>=', 'test'))
    # query.add_filter(filter=PropertyFilter('name', '<', 'test' + '{'))
    query.add_filter(filter=PropertyFilter('house', '=', 'test'))
    print(list(query.fetch()))
    """
    asyncio.run(fetch('test'))

    for i in range(1, len(keys)):
        for com in combinations(keys, i):
            kwarg = base.copy()
            kwarg.update({k: 'test' for k in com})
            asyncio.run(fetch(**kwarg))
