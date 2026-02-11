from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application import error_hundling, middleware


def build(app: FastAPI):
    error_hundling.add_hundler(app=app)
    middleware.bind(app=app)
