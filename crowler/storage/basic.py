from google.cloud import storage
from google.cloud.storage import Bucket

import gzip
from typing import List
from google.cloud.storage import fileio, Blob
import json

from get_metadata import get_metadata

BUCKETS = {}
PROJECT_ID = None
LOCATION = None


def set_location(location):
    global LOCATION
    LOCATION = location


def get_location():
    global LOCATION
    if LOCATION is None:
        LOCATION = '-'.join(get_metadata("zone").split('-')[:-1])
    return LOCATION


def set_project_id(project_id='test'):
    global PROJECT_ID
    PROJECT_ID = project_id


def get_project_id():
    global PROJECT_ID
    if PROJECT_ID is None:
        PROJECT_ID = get_metadata("project_id")

    return PROJECT_ID


def get_bucket(bucket_name: str) -> Bucket:
    global bucket
    if bucket_name not in BUCKETS:

        storage_client = storage.Client()

        _bucket = storage_client.bucket(bucket_name)
        if not _bucket.exists():
            _bucket.create(location=get_location())
        BUCKETS[bucket_name] = _bucket

    return BUCKETS[bucket_name]


class Model:
    bucket: Bucket

    def __init__(self) -> None:
        bucket_name = get_project_id() + '-' + self.__class__.__name__.lower()
        self.bucket = get_bucket(bucket_name)


def upload_gzip(blob: Blob, data):
    if blob.exists():
        return

    json_string = json.dumps(data)

    blob.content_encoding = 'gzip'
    blob.content_type = 'application/json'

    writer = fileio.BlobWriter(blob)

    gz = gzip.GzipFile(fileobj=writer, mode="wb")

    gz.write(json_string.encode('utf-8'))

    gz.close()
    writer.close()
