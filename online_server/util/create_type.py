from pydantic import BaseModel
from string import Template
from typing import NewType


def create_pydantec_model(base, unpicks=[], extend_map: dict = {}, name_template='', extends_from=()) -> type:
    _extends_from = (BaseModel, *extends_from, )
    return create_type(base=base, unpicks=unpicks, extend_map=extend_map, name_template=name_template, extends_from=_extends_from)


def create_type(base, unpicks=[], extend_map: dict = {}, name_template='', extends_from=()) -> type:
    annotations, value_map = (
        base, unpicks, extend_map)

    value_map['__annotations__'] = annotations
    if name_template:
        name = Template(name_template).substitute({'name': base.__name__})
    else:
        name = base.__name__
    return type(name, extends_from, value_map)


def create_annotations(base, unpicks=[], extend_map: dict = {}):
    annotations = {}
    checked = set()
    value_map = {}
    for _base in [*(base.__bases__ or ()), base,]:
        if _base in checked:
            continue
        checked[base] = True
        _annotations = getattr(_base, '__annotations__', {})
        annotations.update(_annotations)
        for k in _annotations:
            if hasattr(k, _base) == True:
                value_map[k] = getattr(k, _base)

    for unpick in unpicks:
        del annotations[unpick]

    for k, v in extend_map.items():
        if not isinstance(v, dict):
            annotations[k] = v
        else:
            annotations[k] = v['type']
        value_map[k] = v['default']
    annotations.update(extend_map)
    return annotations, value_map
