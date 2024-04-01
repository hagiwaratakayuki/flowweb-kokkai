from google.cloud.datastore.query import Query


def check(is_keys_only, query: Query):
    if is_keys_only == True:
        query.keys_only()
