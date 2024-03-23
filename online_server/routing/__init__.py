
from fastapi import FastAPI, APIRouter
from online_server.routing import node
from routing import cluster


routings: list[tuple[str, APIRouter]] = [
    cluster.routing_tuple,
    node.routing_tuple
]


def configure(app: FastAPI):
    for prefix, router in routings:
        app.include_router(prefix=prefix, router=router)
