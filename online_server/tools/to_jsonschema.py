from online_server.routing import node
from routing.return_models.cluster import overview as cluster_overview
from routing.return_models.cluster import overviews as cluster_overviews
from routing.return_models.node import overview as text_overview
from routing.return_models.node import overviews as text_overviews
from routing import cluster
from pydantic import TypeAdapter, BaseModel
import os
import json
import re
import importlib
pt_pyext = re.compile('.py$')
sep_pt = re.compile('[/\\]')


def check_class(target):
    try:
        return issubclass(target, BaseModel)
    except Exception as e:
        return False


modules = [
    cluster,
    node,
    cluster_overview,
    cluster_overviews,
    text_overview,
    text_overviews
]

for root, dirs, files in os.walk('./routing/return_models'):
    modroot = sep_pt.sub('.', root)
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
            file_name = os.path.abspath('../schema/' + name + '.json')

            with open(file_name, "w") as f:
                json.dump(adapter.json_schema(), f, ensure_ascii=False)
