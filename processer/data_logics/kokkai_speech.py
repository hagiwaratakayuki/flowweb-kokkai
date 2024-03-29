from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.speech import Speech


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, session, speeches):

        for data in speeches:

            model = Speech(id=data['id'])
            model.session = session
            model.meeting_id = data['meeting_id']
            model.url = data['url']
            model.order = data['order']
            model.speaker = data['speaker']
            model.speaker_id = data['speaker_id']
            if "response_to" in data:

                model.response_to = data['response_to']
            if "response_from" in data:
                model.response_from = data["response_from"]
            if "discussion_id" in data:
                model.discussion_id = data["discussion_id"]
            self.saver.put(model=model)

    def close(self):
        self.saver.close()
