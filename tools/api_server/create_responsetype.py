from string import Template
from .generate_type_code import generate


module_template_string = """
# This is auto generated. see tools/api_sever/create_responsetype.py 

from pydantic import BaseModel
${imports}

${classes}

"""

module_template = Template(module_template_string)


class_tmaplate_str = """

class ${classname}(BaseModel):
${properties}
"""
class_template = Template(class_tmaplate_str)


def get_targets(module, modpath: str):
    member_name = ''.join([token.capitalize()
                           for token in modpath.split('.')[-2:]])
    return [
        [
            member_name,
            getattr(module, 'Base'),
            getattr(module, 'unpicks', []),
            getattr(module, 'extend_map', {})
        ]
    ]


target_directry = './api_server/routing/return_models/configures'
output_directry = './api_server/routing/return_models/'


def directory_contract(path: str):
    return path


generate(target_directry=target_directry,
         output_directry=output_directry,
         filter_root_func=None,
         class_template=class_template,
         get_targets_func=get_targets,
         module_template=module_template
         )
