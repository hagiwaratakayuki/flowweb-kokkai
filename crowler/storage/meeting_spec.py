import unittest
from unittest.mock import patch, MagicMock
from .meeting import Meeting


class MyTest(unittest.TestCase):
    @patch('storage.meeting.download')
    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    def test_my_function(self,  mock_metatada: MagicMock, mock_storage: MagicMock, mock_downloader: MagicMock):

        mock_metatada.return_value = 'test'
        model = Meeting()
        mock_downloader.side_effect = [['{}', '{}'], []]
        print(list(model.downloadAll()))
