from db.meeting import Meeting


async def fetch(id):
    return await Meeting.get_async(id)
