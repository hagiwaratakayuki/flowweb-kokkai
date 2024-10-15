from .basic import Model, upload_gzip

from .asyncdownloader import download
import json


class Meeting(Model):
    def downloadAll(self):
        session = 1
        self._isContinue = True

        while True:
            yRet = self._getItrable(session=session)

            if self._isContinue == False:
                break

            yield yRet
            session += 1

    def _getItrable(self, session):
        prefix = self._getDir(session)
        blobs = self.bucket.list_blobs(prefix=prefix)

        ret = [json.loads(r) for r in download(blobs=blobs)]

        self._isContinue = len(ret) > 0

        return ret

    def upload(self, session, filename, data):
        filename = self._getDir(session) + '/' + filename
        blob = self.bucket.blob(filename)
        return upload_gzip(blob=blob, data=data)

    def _getDir(self, session):
        return 'session_' + str(session)
