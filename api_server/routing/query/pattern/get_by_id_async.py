from db.model import Model


async def pattern(model: Model, id):
    return await model.get_async(id=id)
