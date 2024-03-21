from pydantic import BaseModel

def create_pydantec_model(name, base, unpicks=[], overwrite: dict = {}):
    annotations = create_annotations(name, base, unpicks, overwrite)
    type(name, (BaseModel,), {'__annotations__': annotations})


def create_types(name, base, unpicks=[], overwrite: dict = {}):
    annotations = create_annotations(name, base, unpicks, overwrite):
    type(name, (), {'__annotations__': annotations})


def create_annotations(name, base, unpicks=[], overwrite: dict = {}):
    annotations = {}
    for _base in set((*(base.__bases__ or ()), base,)):

        annotations.update(getattr(_base, '__annotations__', {}))
    for unpick in unpicks:
        del annotations[unpick]
    annotations.update(overwrite)
    return annotations
