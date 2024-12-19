from typing import Optional, get_type_hints, Iterable
from google.cloud.datastore import Entity


def entity2responsetype_list(responsetype, entities: Iterable[Entity], id_key='id'):
    if entities is None:
        return None
    properties = propertypicker(responsetype)
    return [entity2responsetype(e=e, responsetype=responsetype, properties=properties, id_key=id_key) for e in entities]


def entity2responsetype(responsetype, e: Optional[Entity], id_key='id', properties=None):
    if e is None:
        return None
    _properties = properties or propertypicker(responsetype)
    ret = {}
    ret[id_key] = e.key.id_or_name
    ret.update({k: e.get(k) for k in _properties})
    return ret


def propertypicker(responsetype, id_key='id'):
    return [k for k in get_type_hints(responsetype).keys() if k != id_key and k.find('_') != 0]
