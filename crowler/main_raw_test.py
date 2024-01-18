import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, PropertyMock
from main import app
from const import CROWL_PAST
from application.const import LATEST_SESSION


app.config['TESTING'] = True


class MyTestCase(unittest.TestCase):
    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('main.create_task')
    def test_basic(self,
                   mock_taskcreater: MagicMock,
                   mock_db: MagicMock,
                   mock_metadata_storage: MagicMock,
                   mock_storage: MagicMock):
        mock_metadata_storage.return_value = 'test'

        client = app.test_client()
        result = client.post(CROWL_PAST, json={})
        exist_args, exist_kwargs = mock_taskcreater.call_args
        if len(exist_args) > 0:
            self.assertEqual
        print(exist_kwargs)
