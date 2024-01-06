import datetime
from google.cloud import datastore
import asyncio


async def func1():
    print('func1() started')
    await asyncio.sleep(1)
    print('func1() finished')


async def func2():
    print('func2() started')
    await asyncio.sleep(1)
    print('func2() finished')


# [START datastore_build_service]
# [START datastore_update_entity]
# [START datastore_retrieve_entities]
# [START datastore_delete_entity]


async def add_task(client: datastore.Client, description: str):
    await asyncio.sleep(0)
    # Create an incomplete key for an entity of kind "Task". An incomplete
    # key is one where Datastore will automatically generate an Id
    key = client.key("Task")

    # Create an unsaved Entity object, and tell Datastore not to index the
    # `description` field
    task = datastore.Entity(key, exclude_from_indexes=("description",))

    # Apply new field values and save the Task entity to Datastore
    task.update(
        {
            "created": datetime.datetime.now(tz=datetime.timezone.utc),
            "description": description,
            "done": False,
        }
    )
    client.put(task)
    return task.key


client = datastore.Client()


async def main():
    task1 = asyncio.create_task(func1())
    # task2 = asyncio.create_task(func2())
    task2 = asyncio.create_task(func2())
    await task1
    await task2
    ret = []
    for i in range(10):
        ret.append(i)
    return ret


print(asyncio.run(main()))
# print(add_task(client=client, description='test'))
# main()
