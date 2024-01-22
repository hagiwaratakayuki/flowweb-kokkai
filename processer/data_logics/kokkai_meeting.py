from processer.db.util.chunked_batch_saver import ChunkedBatchSaver
from db.meeting import Meeting


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, meetings):
        for meeting in meetings:
            model = Meeting(id=meeting['id'])
            model.session = meeting['session']

            model.name = meeting['name']
            model.moderator_ids
            model.url = meeting['url']
            model.pdf = meeting['order']
            model.header_text = meeting['header_text']
            moderaters = meeting['moderators']
            model.set_moderators(moderaters)
            model.moderator_ids = list(meeting['moderaters'].values())
            self.saver.put(model)

    def close(self):
        self.saver.close()
