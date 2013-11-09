# coding: utf-8
__author__ = 'petrmatuhov'

from twoodapp import app
from flask import jsonify
from json import JSONDecoder

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/tasklist/add', methods=['POST'])
def add_list():
    from flask import request
    from models import TodoList
    from datetime import datetime


    reply = {}

    code = request.form['code']
    taskdata = request.form['tasklist']
    try:
        tasklist = JSONDecoder.decode(taskdata)
    except:
        reply = {'status': 'error', 'error':'json input decode fail'}
        return jsonify(reply)


    new_list = TodoList()
    new_list.add_time = datetime.now()
    new_list.user_id = 0
    new_list.save()

    return jsonify(reply)