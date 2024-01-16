import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, PropertyMock
from main import app
from const import CROWL_PAST

app.config['TESTING'] = True


class MyTestCase(unittest.TestCase):
    @patch('task.get_metadata')
    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('task.getTV2')
    def test_basic(self,
                   mock_taskloader: MagicMock,
                   mock_db: MagicMock,
                   mock_metadata_storage: MagicMock,
                   mock_storage: MagicMock,
                   mock_metadata_task: MagicMock):
        mock_metadata_storage.return_value = 'test'
        mock_metadata_task.return_value = 'test-sample-a'

        client = app.test_client()
        result = client.post(CROWL_PAST, json={})

        print(result.data)
