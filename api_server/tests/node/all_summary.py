import unittest
from main import app

from fastapi.testclient import TestClient
client = TestClient(app)


class TestAllAymmary(unittest.TestCase):
    def test_basic(self):
        client.get('/node/all_summary')
