
from fastapi import FastAPI, APIRouter
from routing import node, cluster


routings: list[tuple[str, APIRouter]] = [
    cluster.routing_tuple,
    node.routing_tuple
]


def configure_routing(app: FastAPI):
    for prefix, router in routings:
        app.include_router(prefix=prefix, router=router)
