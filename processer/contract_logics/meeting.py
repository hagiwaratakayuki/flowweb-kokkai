from typing import TypedDict, Dict
import json


class ModeratorProtocol(TypedDict):
    moderators: Dict


def decode_moderators_contract(entity: ModeratorProtocol):
    entity['moderators'] = json.loads(entity['moderators'])
    return entity


def encode_moderators_contract(entity: ModeratorProtocol):
    entity['moderators'] = json.dumps(
        entity.get('moderators', []), ensure_ascii=False)
    return entity
