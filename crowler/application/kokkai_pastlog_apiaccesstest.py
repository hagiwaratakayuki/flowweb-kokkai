import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, PropertyMock
from .kokkai_pastlog import crowl
from const import CROWL_PAST
from application.const import LATEST_SESSION


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
        print(crowl({"sessionTo": 166, "startRecord": 201}))
