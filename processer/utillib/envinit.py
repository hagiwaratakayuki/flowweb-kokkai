import configparser
import os

CONFIG = None


def read(group):
    global CONFIG
    envname = os.environ.get('ENVNAME')
    data = None
    if envname is None:
        return {}
    if config is not None:
        if not config:
            return {}
        return config[group]

    config = configparser.ConfigParser()
    paths = [
        os.path.abspath('./envconf/' + envname + '.ini'),
        os.path.abspath('./envconf/' + envname + '_localdev.ini')
    ]

    for path in paths:
        result = config.read(path)
        if len(result) > 0:
            CONFIG = config
            return config[group]
    config = False
