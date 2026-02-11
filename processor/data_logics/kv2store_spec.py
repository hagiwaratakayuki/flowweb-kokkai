import unittest
from unittest.mock import patch, MagicMock

import numpy as np
from data_logics.kv2store import chunker, slot, kv2itr, kv2store


class MyTestCase(unittest.TestCase):
    def test_chunker(self):
        res = list(chunker(range(0, 30), 10, 2))
        self.assertEqual(len(res), 2)
        second_bulk = list(res[1])
        self.assertEqual(len(second_bulk), 1)
        second_bulk_first_chunk = second_bulk[0]
        self.assertEqual(len(second_bulk_first_chunk), 10)
        res = list(chunker(range(0, 31), 10, 2))
        self.assertEqual(len(res), 2)
        second_bulk = list(res[1])
        self.assertEqual(len(second_bulk), 2)
        second_bulk_second_chunk = second_bulk[1]
        self.assertEqual(len(second_bulk_second_chunk), 1)

    @patch('time.sleep')
    def test_slot_sleep(self, sleepmock: MagicMock):
        bulk_itr = chunker(range(0, 30), 10, 2)
        list(slot(bulk_itr=bulk_itr))
        self.assertEqual(sleepmock.call_count, 2)

    @patch('time.sleep')
    def test_slot_not_sleep(self, sleepmock: MagicMock):
        bulk_itr = chunker(range(0, 30), 10, 2)

        list(slot(bulk_itr=bulk_itr, time_range=-1))
        self.assertEqual(sleepmock.call_count, 0)

    @patch('gensim.models.keyedvectors.KeyedVectors.load_word2vec_format')
    def test_kv2itr(self, loader_mock: MagicMock):
        kv_mock = MockKeyedVector()
        loader_mock.return_value = kv_mock
        # print(list(kv2itr()))
        self.assertEqual(set(kv_mock.call_keys),
                         set(kv_mock.key_to_index.keys()))

    @patch('gensim.models.keyedvectors.KeyedVectors.load_word2vec_format')
    @patch('db.model.get_client')
    def test_kv2store(self, put_multi_mock: MagicMock, loader_mock: MagicMock):
        kv_mock = MockKeyedVector()
        loader_mock.return_value = kv_mock
        kv2store()


class MockKeyedVector:
    key_to_index: dict
    call_keys: list

    def __init__(self) -> None:
        self.key_to_index = {'pen': np.array([1, 2]), 'paper': np.array([
            3, 4]), 'ink': np.array([5, 6])}
        self.call_keys = []

    def get_vector(self, key):
        self.call_keys.append(key)

        return self.key_to_index[key]
