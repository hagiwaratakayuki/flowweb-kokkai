import traceback
from flask import Flask, request
from db import memo
from task import create_task
from const import CROWL_PAST
from application import kokkai_pastlog

from const import LOCATION, PROJECT_ID
from storage import basic as storage
storage.set_location(LOCATION)
storage.set_project_id(PROJECT_ID)


app = Flask(__name__)


@app.route("/")
def root():

    payload = {'init': True}
    create_task(payload=payload, in_seconds=1)
    return 'ok'


@app.route("/resume")
def resume():
    payload = {'resume': True}
    create_task(payload=payload, in_seconds=1)
    return 'ok'


@app.route(CROWL_PAST, methods=["POST"])
def crowl():
    try:
        memoModel = memo.Memo.get(id='is_end')
        if memoModel is not None and memoModel.get('value') is not None:
            return

        request_payload = request.get_json(force=True)
        if request_payload.get('resume', False) == True:
            isEnd, next_payload = kokkai_pastlog.resume()
        else:
            isEnd, next_payload = kokkai_pastlog.crowl(request_payload)
        if isEnd != True:

            create_task(payload=next_payload, in_seconds=1)
        else:
            memoModel = memo.Memo(id='is_end')
            memoModel.value = 'yes'
            memoModel.upsert()
            print('crowl done')
    except Exception as e:
        print(r''.join(traceback.format_exception(e)))

    return ''
