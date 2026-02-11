from db.speech import Speech
from google.cloud.datastore.query import PropertyFilter
from routing.entity_types.speech import Speech as SpeechEntity
from routing.query.pattern import cursorfetch
import asyncio


async def fetch(meeting_id):
    await asyncio.sleep(0)
    q = Speech.query()
    q.add_filter(filter=PropertyFilter(
        property_name="meeting_id", operator="=", value=meeting_id))
    q.order = ["sortkey"]
    return q.fetch()
