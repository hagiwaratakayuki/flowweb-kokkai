import logging
from const import CROWL_PAST

from google.protobuf import timestamp_pb2
import datetime
import json
import os
from get_metadata import get_metadata

project = os.environ.get('GOOGLE_CLOUD_PROJECT')
queue = 'default'
LOCATION = None
TV2 = None


def getTV2():
    global TV2
    if TV2 is None:
        from google.cloud import tasks_v2
        TV2 = tasks_v2
    return TV2


def get_location():
    global LOCATION
    '''
    if LOCATION is None:
        LOCATION = '-'.join(get_metadata("zone").split('-')[:-1])
    '''

    # return LOCATION
    return "asia-northeast1"


def create_task(payload, uri=CROWL_PAST, in_seconds=1):

    client = getTV2().CloudTasksClient()

    parent = client.queue_path(project, get_location(), queue)
    # print(project)
    # print(get_location())
    # print(queue)

    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": getTV2().HttpMethod.POST,
            "relative_uri": uri
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["app_engine_http_request"]["headers"] = {
                "Content-type": "application/json"
            }
        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["app_engine_http_request"]["body"] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            seconds=in_seconds
        )

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp

    # Use the client to build and send the task.
    response = client.create_task(parent=parent, task=task)

    return response
