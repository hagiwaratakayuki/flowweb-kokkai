from google.cloud import datastore
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


def get_client():
    global client
    if client is None:
        client = datastore.Client()
    return client


def start_high_bulk():
    is_start_high_bulk = True
    high_bulk_start = time.time()


PT = re.compile(r'^_')


class Model(object):
    _entity_options: dict
    _entity = None

    def __init__(self, id=None, entity_options={}, path_args=[], kwargs={}) -> None:
        global dirs
        self._path_args = path_args
        self._kwargs = kwargs
        self._entity_options = entity_options
        self._id = id

    def get_id(self):
        return self._id

    @classmethod
    def query(cls):

        return get_client().query(kind=cls.__name__)

    def _filter(self, key: str):
        if key.startswith('_') == True:
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
            entity = datastore.Entity(key=key, **options)
        data = {key: self._get_attr(key=key)
                for key in dir(self) if self._filter(key) == True}

        entity.update(data)
        return entity

    def _get_attr(self, key):
        return getattr(self, key)

    @classmethod
    def get_kind(cls):
        return cls.__name__

    @classmethod
    def get(cls, id, *path_args, **kwargs):
        key = cls._get_key(path_args, kwargs, id)
        return get_client().get(key)

    @classmethod
    async def get_async(cls, id, *path_args, **kwargs):
        await asyncio.sleep(0)
        return cls.get(id, *path_args, **kwargs)

    @classmethod
    def get_multi(cls, params) -> Union[List[datastore.Entity], None]:
        return cls._get_multi(params)

    @classmethod
    async def get_multi_async(cls, params) -> Union[List[datastore.Entity], None]:
        await asyncio.sleep(0)
        return cls._get_multi(params)

    @classmethod
    def _get_multi(cls, params):
        params = params or []
        keys = [cls._get_key(**param) for param in params]
        if len(keys) == 0:
            return None

        ret = get_client().get_multi(keys)

        return ret

    @classmethod
    def _get_key(cls, path_args=[], kwargs={}, id=None):

        _path = list(path_args)
        _path.append(cls.__name__)
        if id is not None:
            _path.append(id)
        return get_client().key(*_path, **kwargs)

    def insert(self, *path_args, **kwrgs):
        return self._update(path_args, kwrgs)

    def upsert(self, id=None, *path_args, **kwrgs):
        return self._update(path_args, kwrgs, id)


def put_multi(models: List[Model]):

    entities = [model.get_entity() for model in models]
    get_client().put_multi(entities)
    return entities
