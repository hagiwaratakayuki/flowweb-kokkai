from typing import get_type_hints, Iterable
from google.cloud.datastore import Entity
def typepicker(returntype, entities:Iterable[Entity]):
    properties = [k for k in get_type_hints(returntype).keys() if  k != 'id' and k.find('_') != -1]
    return [returntype(id=e.id, **{k:e.get(k) for k in properties}) for e in entities]
