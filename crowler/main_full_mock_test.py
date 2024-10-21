import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, PropertyMock
from main import app
from const import CROWL_PAST
from application.const import LATEST_SESSION
from lib.webapi.parser_obj.EtreeParser import ParserObject


app.config['TESTING'] = True


class MyTestCase(unittest.TestCase):
    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('core.kokkai.__init__.rest')
    @patch('main.create_task')
    def test_start_crowl(self,
                         mock_taskcreater: MagicMock,
                         mock_restclient: MagicMock,
                         mock_db: MagicMock,
                         mock_metadata_storage: MagicMock,
                         mock_storage: MagicMock):
        client = app.test_client()
        result = client.get('/')
        exist_args, exist_kwargs = mock_taskcreater.call_args
        if len(exist_args) > 0:
            payload = exist_args[0]
        else:
            payload = exist_kwargs['payload']
        print(payload)

    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('core.kokkai.__init__.rest')
    @patch('main.create_task')
    def test_basic(self,
                   mock_taskcreater: MagicMock,
                   mock_restclient: MagicMock,
                   mock_db: MagicMock,
                   mock_metadata_storage: MagicMock,
                   mock_storage: MagicMock):

        mock_metadata_storage.return_value = 'test'
        mockClient = MagicMock()
        parser = ParserObject()

        with open("../testdata/kokkai/212-plane.xml", "r", encoding='utf-8') as file:
            xml = file.read()
            parsed = parser.execute(xml)

        mockClient.send.return_value = (True, parsed,)

        mock_restclient.Client.return_value = mockClient

        client = app.test_client()
        result = client.post(CROWL_PAST, json={'sessionTo': 212})
        exist_args, exist_kwargs = mock_taskcreater.call_args
        if len(exist_args) > 0:
            payload = exist_args[0]
        else:
            payload = exist_kwargs['payload']

        self.assertDictEqual(payload, {'sessionTo': 212, 'startRecord': 4})

    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('core.kokkai.__init__.rest')
    @patch('main.create_task')
    def test_paging(self,
                    mock_taskcreater: MagicMock,
                    mock_restclient: MagicMock,
                    mock_db: MagicMock,
                    mock_metadata_storage: MagicMock,
                    mock_storage: MagicMock):

        mock_metadata_storage.return_value = 'test'
        mockClient = MagicMock()
        parser = ParserObject()

        with open("../testdata/kokkai/212-end.xml", "r", encoding='utf-8') as file:
            xml = file.read()
            parsed = parser.execute(xml)

        mockClient.send.return_value = (True, parsed,)

        mock_restclient.Client.return_value = mockClient

        client = app.test_client()
        result = client.post(CROWL_PAST, json={'sessionTo': 212})
        exist_args, exist_kwargs = mock_taskcreater.call_args
        if len(exist_args) > 0:
            payload = exist_args[0]
        else:
            payload = exist_kwargs['payload']
        print(payload)
        self.assertDictEqual(payload, {'sessionTo': 211})

    @patch('storage.basic.storage')
    @patch('storage.basic.get_metadata')
    @patch('db.model.getDatastoreModule')
    @patch('core.kokkai.__init__.rest')
    @patch('main.create_task')
    def test_end(self,
                 mock_taskcreater: MagicMock,
                 mock_restclient: MagicMock,
                 mock_db: MagicMock,
                 mock_metadata_storage: MagicMock,
                 mock_storage: MagicMock):

        mock_metadata_storage.return_value = 'test'
        mockClient = MagicMock()
        parser = ParserObject()

        with open("../testdata/kokkai/1-end.xml", "r", encoding='utf-8') as file:
            xml = file.read()
            parsed = parser.execute(xml)

        mockClient.send.return_value = (True, parsed,)

        mock_restclient.Client.return_value = mockClient

        client = app.test_client()
        result = client.post(CROWL_PAST, json={'sessionTo': 1})
        print(mockClient.setQueryParamByDict.call_args_list)
        self.assertEqual(mock_taskcreater.call_count, 0)
