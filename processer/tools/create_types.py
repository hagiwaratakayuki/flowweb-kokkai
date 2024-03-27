import os
import pprint
import json
import importlib
from db.model import Model
from pydantic import TypeAdapter, BaseModel
import re
import inspect
import warnings
from collections import deque


warnings.simplefilter('ignore')
pt_pyext = re.compile('\.py$')


for root, dirs, files in os.walk('./db'):
    if root != './db':
        continue
    for file in files:

        if pt_pyext.search(file) is None or file.find('model') != -1:
            continue
        modpath = 'db.' + pt_pyext.sub('', file)
        mod = importlib.import_module(modpath)
        for key in dir(mod):
            target = getattr(mod, key)
            if getattr(target, '__module__', None) != modpath:
                continue

            if not inspect.isclass(target) or not issubclass(target, Model):
                continue
            extended = type(key, (target, BaseModel), {})

            file_name = os.path.abspath('../schema/processer/' + key + '.json')

            with open(file_name, "w") as f:
                json.dump(extended.model_json_schema(), f, ensure_ascii=False)


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
