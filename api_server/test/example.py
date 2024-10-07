from typing import List, Optional, Union
from fastapi import FastAPI
from fastapi.testclient import TestClient
from h11 import Response
from pydantic import BaseModel
from main import app_api

app_api = FastAPI()


class Item(BaseModel):
    msg: str


class Response(BaseModel):
    item: Item
    hoge: Optional[str] = None


@app_api.get("/", response_model=Response)
async def read_main():
    return {'item': Item(**{"msg": "Hello World"})}


client = TestClient(app_api)


def test_read_main():
    response = client.get("/")

    print(response.json())


test_read_main()
