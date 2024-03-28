

from collections import defaultdict

import importlib
import inspect
from operator import itemgetter
from string import Template
from typing import Tuple, TypedDict
from db.model import Model
from util import create_type
import os
import re


module_template_string = """
from typing import DefaultDict
${imports}

${classes}

"""

module_template = Template(module_template_string)

import_class_template_str = """${name} as ${as_alias} """

import_class_template = Template(import_class_template_str)

import_template_str = """from ${module} import ${import_classes} """

import_template = Template(import_template_str)

class_tmaplate_str = """
class ${classname}(DefaultDict):
${properties}
"""
class_template = Template(class_tmaplate_str)


property_template_string = """    ${name}:${type}"""
property_template = Template(property_template_string)


def alias_contract(tokens):
    return '_'.join(tokens)


def directory_contract(path: str):
    return path.replace('db.', 'routing.entity_types.')


pt_pyext = re.compile('\.py$')
pt_args = re.compile('[\s,\]\[]+')
for root, dirs, files in os.walk('./db'):
    if root != './db':
        continue
    for file in files:
        if pt_pyext.search(file) is None or file.find('model') != -1 or file == '__init__.py':
            continue

        modpath = 'db.' + pt_pyext.sub('', file)
        mod = importlib.import_module(modpath)
        imported_modules = defaultdict(dict)
        required_imports = []
        class_strs = []
        for key in dir(mod):
            target = getattr(mod, key)
            if getattr(target, '__module__', None) != modpath:
                continue

            if not inspect.isclass(target) or not issubclass(target, Model):
                continue
            annotations, value_map = create_type.create_annotations(
                base=target)
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
                        mod_name = directory_contract('.'.join(splited[:-1]))
                        class_name = splited[-1]

                        as_alias = alias_contract(splited)
                        imported_modules[mod_name][class_name] = as_alias
                        dot_count = len(splited)
                        replaces.append((dot_count, pathed_class, as_alias,))
                    sorted(replaces, key=itemgetter(0), reverse=True)
                    for dot_count, pathed_class, as_alias in replaces:
                        type_string = type_string.replace(
                            pathed_class, as_alias)

                else:

                    type_module = getattr(type_cls, '__module__', None)
                    type_string = ''
                    if type_module != None and type_module != 'builtins' and type_module != modpath:

                        type_module = directory_contract(type_module)
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
                    {'name': name, 'type': type_string})

                properties.append(property_str)

            properties_str = '\n'.join(properties)
            class_str = class_template.substitute(
                {'classname': key, 'properties': properties_str})
            class_strs.append(class_str)
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

        file_name = os.path.abspath(
            './routing/entity_types/' + file)

        with open(file_name, "w") as f:
            f.write(module_str)
