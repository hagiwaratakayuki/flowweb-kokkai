from db.model import Model


def pattern(model: Model, id):
    return model.get_async(id=id)
