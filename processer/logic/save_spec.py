import unittest
import random
import string

from unittest.mock import patch, MagicMock
from .save import buildModel, Logic
import numpy as np
from data_loader.dto import BaseDataDTO
from doc2vec.indexer.dto import build_mock_sentiment_result
import random
import datetime
import calendar
from lorem_text import lorem


class MyTestCase(unittest.TestCase):

    def test_basic(self):
        keyword_map = [
            create_dummy_string()
            for n in range(random.randint(5, 20))

        ]
        keywords_len = len(keyword_map)
        keywords_indexs_count = keywords_len - 1
        n_samples = 100
        keywords = [

            [keyword_map[random.randint(0, keywords_indexs_count)]
             for n in range(random.randint(1, keywords_len))]

            for i in range(n_samples)
        ]
        datas = [BaseDataDTO(body=lorem.sentence(), title='', data={}, author=create_dummy_string(
        ), authorid=create_dummy_string(), published=get_random_date(2014, 2023)) for i in range(n_samples)]
        vectors = np.random.rand(n_samples, 10)
        sentiments = [build_mock_sentiment_result(
            d1=10) for i in range(n_samples)]

        db_model = buildModel()

        with patch("db.model.client") as client_mock:
            logic = Logic()

            print(logic.save(datas=list(
                zip(vectors, sentiments, keywords, datas)), model=db_model))


def get_random_date(startYear, endYear):
    year = random.randint(startYear, endYear)
    month = random.randint(1, 12)
    dateEnd = calendar.monthrange(year=year, month=month)[1]
    day = random.randint(1, dateEnd)
    return datetime.datetime(year=year, month=month, day=day)


def create_dummy_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 10))])
