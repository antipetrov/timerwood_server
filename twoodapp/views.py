# coding: utf-8
__author__ = 'petrmatuhov'

from twoodapp import app,db
from flask import jsonify
from json import JSONDecoder

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/timer/save', methods=['POST'])
def add_list():
    from flask import request
    from models import Timer
    from datetime import datetime
    import uuid
    import random

    reply = {}

    code = request.form.get('code', 0)
    data = request.form['data']
    try:
        parsed_data = JSONDecoder.decode(data)
    except:
        reply = {'status': 'error', 'error': 'json input decode fail'}
        return jsonify(reply)

    if code != 0:
        # save into existing timer
        timer_found = Timer.query.get(Timer.master_code==code)
        timer_found.timer_data = data
        timer_found.edit_time = datetime.now()
        db.session.add(timer_found)
    else:
        # create new timer
        new_timer = Timer()
        new_timer.create_time = datetime.now()
        new_timer.timer_data = data
        new_timer.master_code = uuid.uuid1()
        db.session.add(new_timer)



    return jsonify(reply)