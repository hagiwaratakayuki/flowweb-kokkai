from typing import List, Optional, Union
from fastapi import FastAPI
from fastapi.testclient import TestClient
from h11 import Response
from pydantic import BaseModel
from main import app

app = FastAPI()


class Item(BaseModel):
    msg: str


class Response(BaseModel):
    item: Item
    hoge: Optional[str] = None


@app.get("/", response_model_exclude_none=True)
async def read_main():
    return {'item': Item(**{"msg": "Hello World"})}


client = TestClient(app)


def test_read_main():
    response = client.get("/")

    print(response.json())


test_read_main()
