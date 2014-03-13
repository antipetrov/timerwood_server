# coding: utf-8
__author__ = 'petrmatuhov'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# load config
import settings

# init app
app = Flask(__name__)
app.config.from_object(settings)

# start db
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *


# api entry points
from flask.views import View, MethodView
from flask import request,jsonify
import json
import datetime


class TaskListApi(MethodView):
    #get list
    def get(self, timer_code):
        return 'tasklist get %s\n' % timer_code

    # create
    def post(self, timer_code):
        import short_url, random, string

        alphabet = string.ascii_letters + string.digits + "*%&$"

        if not timer_code:
            timer_code = ''.join(random.choice(alphabet) for x in range(8))

        guest_code = ''.join(random.choice(alphabet) for x in range(10))
        timer_data = request.form['data']

        newTimer = models.Timer()
        newTimer.create_time = datetime.datetime.now()
        newTimer.edit_time = datetime.datetime.now()
        newTimer.master_code = timer_code
        newTimer.guest_code = guest_code
        newTimer.timer_data = timer_data

        db.session.add(newTimer)
        db.session.commit()

        result = {
            'status': True,
            'master_code': newTimer.master_code,
            'guest_code': newTimer.guest_code,
        }

        return json.dumps(result)

    #update
    def put(self, timer_code):
        return 'tasklist put %s\n' % timer_code

    # remove
    def delete(self, timer_code):
        return 'tasklist delete %s\n' % timer_code


timer_api_view = TaskListApi.as_view('admin_api')

app.add_url_rule('/timer/<string:timer_code>/', view_func=timer_api_view, methods=['GET', ])
app.add_url_rule('/timer/', view_func=timer_api_view, methods=['POST', ], defaults={'timer_code': None})
app.add_url_rule('/timer/<string:timer_code>/', view_func=timer_api_view, methods=['PUT', ])