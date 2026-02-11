from fastapi import FastAPI
from typing import Any
from ..middleware import cors

middlewares: list[tuple[Any, dict]] = [cors.middleware]


def bind(app: FastAPI):
    for middleware_class, init in middlewares:
        app.add_middleware(middleware_class, **init)
