# run by python -m

from unittest.mock import MagicMock, patch
from application.kokkai_pastlog import createDataAndFileName
from core.kokkai import search
from lib.webapi.parser_obj.EtreeParser import ParserObject
import os
import json

with patch('core.kokkai.rest') as mockRest:

    mockClient = MagicMock()
    parser = ParserObject()

    with open(os.path.join(os.getcwd(), "../testdata/kokkai/212-plane.xml"), "r", encoding='utf-8') as file:
        xml = file.read()
        parsed = parser.execute(xml)

    mockClient.send.return_value = (True, parsed,)

    mockRest.Client.return_value = mockClient
    res = search({})
    if res:
        data, filename = createDataAndFileName(res.records)
        with open(os.path.join(os.getcwd(), "../testdata/kokkai/212-plane.json"), "w", encoding='utf-8') as file:
            json.dump(obj=data, fp=file)
