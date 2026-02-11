import importlib
import sys
import os
import re
target_directory = os.path.abspath('./api_server')

sys.path.append(target_directory)
pt_sep = re.compile(r'[\\\/]+')
pt_pyext = re.compile(r'\.py$')


def generate():

    for root, dirs, files in os.walk(os.path.join(target_directory, './routing/query')):

        reguraized_root_path = os.path.abspath(
            root).replace(target_directory, '')
        base_mod_path = '.'.join(
            [token for token in pt_sep.split(reguraized_root_path) if token != ''])
        for file in files:
            if pt_pyext.search(file) is None or file.find('model') != -1 or file == '__init__.py':
                continue

            modpath = base_mod_path + '.' + pt_pyext.sub('', file)

            mod = importlib.import_module(modpath)
            mod_dir = dir(mod)
            if 'indexer' in mod_dir:
                print(modpath)
                mod.indexer()


generate()
