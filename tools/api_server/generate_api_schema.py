import sys
import os
import importlib
from fastapi.openapi.utils import get_openapi


def main():
    sys.path.append(os.path.abspath('./api_server'))
    app = importlib.import_module('main').app
    print(get_openapi(title='api server', version='1.0', routes=app.routes))


main()
