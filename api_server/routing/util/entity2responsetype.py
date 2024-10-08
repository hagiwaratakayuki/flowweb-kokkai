from typing import get_type_hints, Iterable
from google.cloud.datastore import Entity


def entity2responsetype_list(responsetype, entities: Iterable[Entity], id_key='id'):
    properties = propertypicker(responsetype)
    return [entity2responsetype(e=e, responsetype=responsetype, properties=properties, id_key=id_key) for e in entities]


def entity2responsetype(responsetype, e: Entity, id_key='id', properties=None):
    _properties = properties or propertypicker(responsetype)
    ret = {}
    ret[id_key] = e.id
    ret.update({k: e.get(k) for k in _properties})
    return ret


def propertypicker(responsetype):
    return [k for k in get_type_hints(responsetype).keys() if k != 'id' and k.find('_') != 0]
