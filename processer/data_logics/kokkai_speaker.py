from typing import Dict
from db.util.chunked_batch_saver import ChunkedBatchSaver
from db.speaker import Speaker

keys = ["group",  "position",   "role"]


class Saver:
    def __init__(self) -> None:
        self.saver = ChunkedBatchSaver()

    def save(self, speaker_id_map: Dict[str, Dict]):
        for speaker_id, speaker in speaker_id_map.items():
            model = Speaker(id=speaker_id)
            model.session = speaker['session']

            model.name = speaker['name']
            for key in keys:
                if key in speaker:
                    setattr(model, key, speaker[key])
            self.saver.put(model)

    def close(self):
        self.saver.close()
