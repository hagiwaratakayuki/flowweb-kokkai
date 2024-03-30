from fastapi import FastAPI
from app import builder
import routing 

app = FastAPI()
builder.build(app=app)
routing.configure(app=app)