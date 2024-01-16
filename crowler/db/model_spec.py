import unittest
from operator import itemgetter
from unittest.mock import patch,MagicMock, call
from .model import Model, put_multi

class TestModel (Model):
    target:str

class MyTestCase(unittest.TestCase):

    @patch("db.model.client")
    def test_multi(self, client_patch:MagicMock):
        entity = TestModel(id=1)
        entity.target = 'test'
        put_multi([entity])
        self.assertIn(call.key('TestModel', 1), client_patch.mock_calls)
        self.assertEqual(client_patch.mock_calls[1].args[0][0]['target'], 'test')
    @patch("db.model.client")
    def test_put_new(self, client_patch:MagicMock):
        entity = TestModel()
        entity.target = 'test'
        entity.insert()
        
        self.assertIn(call.key('TestModel'), client_patch.mock_calls, 'valid key call')
        self.assertIn(call.put(entity.get_entity()), client_patch.mock_calls, 'valid enity call')
    @patch("db.model.client")   
    def test_get(self, client_patch:MagicMock):
        key_mock = MagicMock()
        client_patch.key = key_mock
        key_mock.return_value = 'test'
         
        e = TestModel.get(1) 
        
        
        self.assertIn(call.key('TestModel', 1), client_patch.mock_calls, 'valid key call')
        self.assertIn(call.get('test'), client_patch.mock_calls, 'valid key call')
        

    

