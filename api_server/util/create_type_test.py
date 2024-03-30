from .create_type import create_pydantec_model, create_annotations, create_type
import unittest
from typing import Union


from typing import Union

from pydantic import BaseModel, Field, ValidationError
from db.proxy import Node


class User(BaseModel, Node):
    pass


class MockClass:
    example: str
    weights: str


extend_map = {
    'position': {
        'type': Union[str, int],
        'default': None
    }
}


class Test(unittest.TestCase):
    def test_create_pydantic_model(self):
        """
        create_pydantec_model(name_template="example",  base=MockClass, unpicks=[
            'weights'], extend_map=extend_map)
        """
