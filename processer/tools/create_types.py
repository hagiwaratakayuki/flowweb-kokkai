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
pt_pyext = re.compile(r'\.py$')


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
