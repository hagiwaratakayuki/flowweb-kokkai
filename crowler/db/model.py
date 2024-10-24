
import re

from collections.abc import Iterable
from typing import List, Literal, Any, Union
import time
import asyncio


client = None
is_start_high_bulk = False
high_bulk_limit_base = 500
high_bulk_step_range = 0.5
high_bulk_limit = high_bulk_limit_base
high_bulk_start = 0
DATASTORE = None


def get_client():
    global client
    if client is None:

        client = getDatastoreModule().Client()
    return client


def getDatastoreModule():
    global DATASTORE
    if DATASTORE is None:
        from google.cloud import datastore
        DATASTORE = datastore
    return DATASTORE


def start_high_bulk():
    is_start_high_bulk = True
    high_bulk_start = time.time()


PT = re.compile(r'^_')


class Model(object):
    _entity_options: dict

    def __init__(self, id=None, entity_options={}, path_args=[], kwargs={}) -> None:
        self._path_args = path_args
        self._kwargs = kwargs
        self._entity_options = entity_options
        self._id = id
        self._entity = None

    @classmethod
    def query(cls):

        return get_client().query(kind=cls.__name__)

    def _filter(self, key):
        if PT.search(key) is not None:
            return False
        if callable(getattr(self, key)):
            return False
        return True

    def _update(self, path_args=None, kwargs=None, id=None):
        id = id or self._id
        path_args = path_args or self._path_args
        kwargs = kwargs or self._kwargs

        client = get_client()
        with client.transaction():
            entity = self.get_entity(id, path_args, kwargs)

            client.put(entity)
        return entity

    def get_entity(self, id=None, path_args=None, kwargs=None):
        if self._entity != None:
            entity = self._entity
        else:
            options = self._entity_options
            key = self.__class__._get_key(
                path_args or self._path_args, kwargs or self._kwargs, id or self._id)
            entity = getDatastoreModule().Entity(key=key, **options)
        data = {key: getattr(self, key)
                for key in filter(self._filter, dir(self))}

        entity.update(data)
        return entity

    @classmethod
    def get_kind(cls):
        return cls.__name__

    @classmethod
    def get(cls, id, *path_args, **kwargs):
        key = cls._get_key(path_args, kwargs, id)
        return get_client().get(key)

    @classmethod
    def get_multi(cls, params, is_trict: bool = False):
        if params == None or not isinstance(Iterable, params):
            return None
        keys = [cls._get_key(**param) for param in params]
        if len(keys) == 0:
            return None

        ret = get_client().get_multi(keys)
        if is_strict == True and ret.count(None) > 0:  # type: ignore
            return None
        return ret

    @classmethod
    def _get_key(cls, path_args=[], kwargs={}, id=None):

        _path = list(path_args[:])
        _path.append(cls.__name__)
        if id is not None:
            _path.append(id)
        return get_client().key(*_path, **kwargs)

    def insert(self, *path_args, **kwrgs):
        return self._update(path_args, kwrgs)

    def upsert(self, id=None, *path_args, **kwrgs):
        return self._update(path_args, kwrgs, id)

    @classmethod
    def from_entity(cls, entity):
        ret = cls()
        for k, v in entity.items():
            setattr(ret, k, v)
        ret._entity = entity
        return ret

    def put(self):
        get_client().put(self.get_entity())


def put_multi(models: Iterable[Model]):
    entities = [model.get_entity() for model in models]
    get_client().put_multi(entities)
    return entities

# todo


def put_as_high_bulk(models: Iterable[Model]) -> Literal['enqueue', 'exec']:
    loop = asyncio.get_event_loop()
    # loop.run_in_executor()
    return 'enqueue'
