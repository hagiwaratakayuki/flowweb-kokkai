
import sys
from pydantic import TypeAdapter, BaseModel
import os
import json
import re
import importlib
pt_pyext = re.compile(r'.py$')
sep_pt = re.compile(r'(\\|/)+')
new_import_path = os.path.abspath('./api_server/')
sys.path.append(new_import_path)


def check_class(target):
    try:
        return issubclass(target, BaseModel)
    except Exception as e:
        return False


for root, dirs, files in os.walk('./api_server/routing/return_models'):
    modroot = root.replace('/', '.').replace('\\', '.').replace('..', '')

    for file in files:

        if pt_pyext.search(file) is None:
            continue

        modpath = modroot + '.' + pt_pyext.sub('', file)
        module = importlib.import_module(modpath)

        for name in dir(module):

            if name.find('_') == 0:
                continue
            target = getattr(module, name)

            if not hasattr(target, '__module__'):
                continue

            target_module_name = str(target.__module__)
            if target_module_name != modpath or target_module_name.find('pydantic') != -1 or check_class(target) == False:
                continue

            adapter = TypeAdapter(target)
            file_name = os.path.abspath('./schema/' + name + '.json')

            with open(file_name, "w") as f:
                json.dump(adapter.json_schema(), f, ensure_ascii=False)
