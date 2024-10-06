from fastapi import FastAPI
from application import builder
from routing import configure_routing

app_api = FastAPI()
builder.build(app=app_api)
configure_routing(app=app_api)
