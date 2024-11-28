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
        model.keywords = meeting['keywords']

        model.moderators = meeting['moderators']
        model.moderator_ids = list(meeting['moderators'].values())
        self.saver.put(model)

    def close(self):
        self.saver.close()
