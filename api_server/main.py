from fastapi import FastAPI
from application import builder
from routing import configure_routing

app = FastAPI()
builder.build(app=app)
configure_routing(app=app)
