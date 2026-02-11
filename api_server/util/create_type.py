from collections import deque
from pydantic import BaseModel
from string import Template


def create_pydantec_model(base, unpicks=[], extend_map: dict = {}, name_template='', extends_from=()) -> type:
    return
    _extends_from = (BaseModel, *extends_from, )
    return create_type(base=base, unpicks=unpicks, extend_map=extend_map, name_template=name_template, extends_from=_extends_from)


def create_type(base, unpicks=[], extend_map: dict = {}, name_template='', extends_from=()) -> type:
    return
    annotations, value_map = create_annotations(
        base, unpicks, extend_map)

    value_map['__annotations__'] = annotations
    if name_template:
        name = Template(name_template).substitute({'name': base.__name__})
    else:
        name = base.__name__
    return type(name, extends_from, value_map)


def create_annotations(base, unpicks=[], extend_map: dict = {}):

    annotations = {}
    base_checked = {}
    checked = {}

    value_map = {}
    bases = deque()
    bases.append(base)

    while len(bases) != 0:
        _base = bases[0]
        if _base in checked:
            continue
        if _base not in base_checked and not not _base.__bases__:
            bases.extendleft(_base.__bases__)
            base_checked[_base] = True
            continue
        base_checked[_base] = True
        checked[_base] = True
        bases.popleft()

        _annotations = {k: v for k, v in getattr(
            _base, '__annotations__', {}).items() if k.find('_') != 0}

        annotations.update(_annotations)

        for k in _annotations.keys():

            if hasattr(_base, k) == True:
                value_map[k] = getattr(_base, k)

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
