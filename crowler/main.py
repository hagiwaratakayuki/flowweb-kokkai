from flask import Flask, request
from task import create_task
from const import CROWL_PAST
from application import kokkai_pastlog

app = Flask(__name__)


@app.route("/")
def root():
    payload = {'init': True}
    create_task(pyload=payload, in_seconds=None)
    return 'ok'


@app.route(CROWL_PAST, methods=["POST"])
def crowl():
    request_paylod = request.get_json(force=True)
    isEnd, next_payload = kokkai_pastlog.crowl(request_paylod)
    if isEnd != True:
        create_task(pyload=next_payload)

    return ''
