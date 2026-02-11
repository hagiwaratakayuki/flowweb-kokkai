from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.speech import Speech
from db import meeting


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, session, speeches):

        for speech in speeches:

            model = Speech(id=speech['id'])
            model.session = session
            model.meeting_id = speech['meeting_id']
            model.meeting = speech['meeting']
            model.url = speech['url']
            model.order = speech['order']
            model.speaker = speech['speaker']
            model.speaker_id = speech['speaker_id']
            model.title = speech['title']
            model.house = speech['house']
            model.issue = speech['issue']

            model.sortkey = '_'.join(
                [str(k).zfill(3) for k in [session, speech['issue'], speech['order']]])
            if "response_to" in speech:

                model.response_to = speech['response_to']
            if "response_from" in speech:
                model.response_from = speech["response_from"]
            if "discussion_id" in speech:
                model.discussion_id = speech["discussion_id"]
            self.saver.put(model=model)

    def close(self):
        self.saver.close()
