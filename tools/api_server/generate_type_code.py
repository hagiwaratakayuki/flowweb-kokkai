

from collections import defaultdict

from collections.abc import Iterable
import importlib
import inspect
from operator import itemgetter
from string import Template as TemplateCls
from typing import Any, Callable, Dict, Optional, Tuple, TypedDict, Union
from api_server.db.model import Model
from tools.util import create_type
import os
import re
import sys


default_module_template_string = """
from .basetype import BaseType
${imports}

${classes}

"""

default_module_template = TemplateCls(default_module_template_string)

import_class_template_str = """${name} as ${as_alias} """

import_class_template = TemplateCls(import_class_template_str)

import_template_str = """from ${module} import ${import_classes} """

import_template = TemplateCls(import_template_str)

default_class_tmaplate_str = """
class ${classname}(BaseType):
${properties}
"""
default_class_template = TemplateCls(default_class_tmaplate_str)


property_template_string = """    ${name}: ${type}"""
property_template = TemplateCls(property_template_string)


def default_alias_contract(tokens):
    return '_'.join(tokens)


def default_import_contract(path: str):
    return path.replace('db.', 'routing.entity_types.')


def filter_root(root: str):
    return root != './api_server/db'


def get_targets(module, modpath):
    for key in dir(module):
        target = getattr(module, key)
        if getattr(target, '__module__', None) != modpath:
            continue

        if not inspect.isclass(target) or not issubclass(target, Model):
            continue
        yield key, target, [], {}


pt_pyext = re.compile(r'\.py$')
pt_args = re.compile(r'[\s,\]\[]+')
pt_sep = re.compile(r'[\\\/]+')


def generate(target_directry='./api_server/db',
             output_directry='./api_server/routing/entity_types/',
             filter_root_func: Optional[Callable] = filter_root,
             class_template: TemplateCls = default_class_template,
             module_template: TemplateCls = default_module_template,
             get_targets_func: Callable[[
                 Any, str], Iterable[Tuple[str, type, list[str], Dict]]] = get_targets,
             import_contract=default_import_contract,
             alias_contract=default_alias_contract
             ):
    new_path_list = []
    for token in pt_sep.split(target_directry):
        new_path_list.append(token)
        if token != '.':
            break

    new_import_path = os.path.abspath(os.path.sep.join(new_path_list))
    sys.path.append(new_import_path)

    for root, dirs, files in os.walk(target_directry):
        reguraized_root_path = os.path.abspath(root).replace(os.getcwd(), '')
        base_mod_path = '.'.join(
            [token for token in pt_sep.split(reguraized_root_path) if token != ''])

        if filter_root_func is not None and filter_root_func(root) == True:
            continue
        _output_directry = root.replace(target_directry, output_directry, 1)
        is_directry_checked = False
        for file in files:
            if pt_pyext.search(file) is None or file.find('model') != -1 or file == '__init__.py':
                continue

            modpath = base_mod_path + '.' + pt_pyext.sub('', file)
            mod = importlib.import_module(modpath)
            imported_modules = defaultdict(dict)
            required_imports = []
            class_strs = []
            for member_name, target, unpicks, extend_map, picks in get_targets_func(mod, modpath):

                annotations, value_map = create_type.create_annotations(
                    base=target, unpicks=unpicks, extend_map=extend_map, picks=picks)
                properties = []

                for name, type_cls in annotations.items():
                    if name.find('_') == 0:
                        continue
                    if hasattr(type_cls, '__args__'):

                        replaces: list[Tuple[int, str, str]] = []

                        type_string = str(type_cls)

                        for pathed_class in pt_args.split(type_string):

                            if not pathed_class:
                                continue
                            splited = pathed_class.split('.')
                            if len(splited) == 1:
                                continue
                            mod_name = import_contract(
                                '.'.join(splited[:-1]))
                            class_name = splited[-1]

                            as_alias = alias_contract(splited)
                            imported_modules[mod_name][class_name] = as_alias
                            dot_count = len(splited)
                            replaces.append(
                                (dot_count, pathed_class, as_alias,))
                        sorted(replaces, key=itemgetter(0), reverse=True)
                        for dot_count, pathed_class, as_alias in replaces:
                            type_string = type_string.replace(
                                pathed_class, as_alias)

                    else:

                        type_module = getattr(type_cls, '__module__', None)
                        type_string = ''
                        if type_module != None and type_module != 'builtins' and type_module != modpath:

                            type_module = import_contract(type_module)
                            class_name = getattr(type_cls, '__name__', None) or getattr(
                                type_cls, '_name')
                            as_alias = alias_contract(
                                [*type_module.split('.'), class_name])
                            imported_modules[type_module][class_name] = as_alias
                            type_string = as_alias
                        else:
                            type_string = getattr(
                                type_cls, '__name__', None) or getattr(type_cls, '_name')

                    property_str = property_template.substitute(
                        {'name': name, 'type': type_string}).replace('NoneType', 'Type[None]')

                    properties.append(property_str)

                properties_str = '\n'.join(properties)
                class_str = class_template.substitute(
                    {'classname': member_name, 'properties': properties_str})
                class_strs.append(class_str)
            if len(class_strs) == 0:
                continue
            for module, alias_map in imported_modules.items():
                import_classes = []
                for name, as_alias in alias_map.items():
                    import_class = import_class_template.substitute(
                        dict(name=name, as_alias=as_alias))
                    import_classes.append(import_class)
                required_import = import_template.substitute(
                    dict(module=module, import_classes=', '.join(import_classes)))
                required_imports.append(required_import)
            required_imports_str = '\n'.join(required_imports)

            module_str = module_template.substitute(
                {'classes': '\n'.join(class_strs), 'imports': required_imports_str})

            file_name = os.path.join(_output_directry, file)
            if is_directry_checked == False:
                target_dir = os.path.dirname(file_name)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                is_directry_checked = True
            with open(file_name, "w") as f:
                f.write(module_str)
