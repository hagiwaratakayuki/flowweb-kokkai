from fastapi import FastAPI
from ..error_hundling import status_exception
binders = [status_exception.binder]


def add_hundler(app: FastAPI):
    for binder in binders:
        binder(app)
