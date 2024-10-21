# import traceback
from tkinter import N
from flask import Flask, request
from db import memo
from task import create_task
from const import CROWL_PAST
from application import kokkai_pastlog
import logging
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
    memoModel = memo.Model.get(id='is_end')
    if memoModel is not None and memoModel.get('value') is not None:
        return

    request_paylod = request.get_json(force=True)
    if request_paylod.get('resume', False) == True:
        isEnd, next_payload = kokkai_pastlog.resume()
    else:
        isEnd, next_payload = kokkai_pastlog.crowl(request_paylod)
    if isEnd != True:

        create_task(payload=next_payload, in_seconds=1)
    else:
        memoModel = memo.Model(id='is_end')
        memoModel.value = 'yes'
        memoModel.upsert()
        print('crowl done')

    return ''
