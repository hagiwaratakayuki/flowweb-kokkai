
import asyncio
from db.meeting import Meeting
from ..pattern import cursorfetch


async def fetch(keyword=None, issue=None, session=None, name=None, cursor_str=None, limit=10):
    if keyword == None and issue == None and session == None and name == None:
        return False
    asyncio.sleep(0)
    query = Meeting.query()
    if (not keyword) == False:
        query.add_filter('keyword', '=', keyword)
    if (not issue) == False:
        query.add_filter('issue', '=', issue)
    if (not session) == False:
        query.add_filter('name', '=', name)
    query.projection = ['keyword', 'issue', 'session', 'name']

    return cursorfetch.fetch(query=query, cursor=cursor_str, limit=limit)
