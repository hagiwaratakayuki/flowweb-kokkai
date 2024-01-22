import random
import string
from data_logics.save import buildModel, _save

import numpy as np
from data_loader.dto import DTO
from doc2vec.indexer.dto import build_mock_sentiment_result
import datetime
import calendar
import lorem


def main():

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
    datas = [DTO(body=lorem.sentence(), title='', data={}, speaker=create_dummy_string(
    ), authorid=create_dummy_string(), published=get_random_date(2014, 2023)) for i in range(n_samples)]
    vectors = np.random.rand(n_samples, 10)
    sentiments = [build_mock_sentiment_result(d1=10) for i in range(n_samples)]

    db_model = buildModel()

    print(_save(datas=list(zip(vectors, sentiments, keywords, datas)), model=db_model))


def get_random_date(startYear, endYear):
    year = random.randint(startYear, endYear)
    month = random.randint(1, 12)
    dateEnd = calendar.monthrange(year=year, month=month)[1]
    day = random.randint(1, dateEnd)
    return datetime.datetime(year=year, month=month, day=day)


def create_dummy_string():
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 10))])


if __name__ == '__main__':

    main()
