from .const import CROWL_PAST
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime
import json
import os


# TODO(developer): Uncomment these lines and replace with your values.
project = os.environ.get('GOOGLE_CLOUD_PROJECT')
queue = 'default'
location = 'us-central1'


def create_task(pyload, uri=CROWL_PAST, in_seconds=1):
    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "app_engine_http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
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

    print(f"Created task {response.name}")
    return response
