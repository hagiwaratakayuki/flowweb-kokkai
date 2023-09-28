from fastapi import FastAPI
from online_server.app.error_hundling import status_exception
binders = [status_exception.binder]


def add_hundler(app:FastAPI):
    for binder in binders:
        binder(app)