import datetime
import json
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.meeting import Meeting


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, meeting):

        model = Meeting(id=meeting['id'])
        model.session = meeting['session']
        model.issue = meeting['issue']

        model.name = meeting['name']

        model.url = meeting['url']
        model.pdf = meeting['pdf']
        model.header_text = meeting['headerRecord']

        model.house = meeting['house']
        moderaters = []
        moderater_ids = []
        for moderater_data in meeting['moderators'].values():
            moderater = {'id': moderater_data['id'],
                         'name': moderater_data['speaker']}
            if 'group' in moderater_data['speaker']:
                moderater['group'] = moderater_data['speaker']['group']
            moderaters.append(moderater)
            moderater_ids.append(moderater_data['id'])

        model.moderators = moderaters
        model.moderator_ids = moderater_ids
        model.create_at = datetime.datetime.now().isoformat()
        model.update_at = datetime.datetime.now().isoformat()
        self.saver.put(model)

    def close(self):
        self.saver.close()
