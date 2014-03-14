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

import models


# api entry points
from flask.views import View, MethodView
from flask import request,jsonify
import json
import datetime


class TaskListApi(MethodView):
    #get list
    def get(self, timer_code):

        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            result = {'status': False, 'error': 'Timer %s not found' % timer_code}
        else:
            result = {'status': True, 'mode': found_code.code_type, 'data': found_code.timer.timer_data}

        return jsonify(result)

    # create
    def post(self, timer_code):
        import short_url, random, string

        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if found_code:
            return jsonify({'status': False, 'error': 'Timer %s already exists' % found_code.code})

        #save timer data
        timer_data = request.form['data']

        newTimer = models.Timer()
        newTimer.create_time = datetime.datetime.now()
        newTimer.edit_time = datetime.datetime.now()
        newTimer.timer_data = timer_data
        db.session.add(newTimer)
        db.session.flush()


        # create codes
        alphabet = string.ascii_letters + string.digits + "%&$"

        if not timer_code:
            timer_code = ''.join(random.choice(alphabet) for x in range(8))

        guest_code = ''.join(random.choice(alphabet) for x in range(9))

        # add master code
        newTimerCode = models.TimerCode()
        newTimerCode.timer_id = newTimer.id
        newTimerCode.code_type = 'master'
        newTimerCode.code = timer_code
        db.session.add(newTimerCode)

        # add master code
        newGuestCode = models.TimerCode()
        newGuestCode.timer_id = newTimer.id
        newGuestCode.code_type = 'guest'
        newGuestCode.code = guest_code
        db.session.add(newGuestCode)

        db.session.commit()

        return jsonify({
            'status': True,
            'master_code': timer_code,
            'guest_code': guest_code,
        })

    #update
    def put(self, timer_code):
        return 'tasklist put %s\n' % timer_code

    # remove
    def delete(self, timer_code):
        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            return jsonify({'status': False, 'error': "Timer not found"})

        if not found_code.code_type == 'master':
            return jsonify({'status': False, 'error': "Operation not permitted"})
        else:

            timer = found_code.timer

            models.TimerCode.query.filter(models.TimerCode.timer == timer).delete()
            db.session.delete(timer)
            db.session.commit()

            try:
                db.session.commit()
            except Exception:
                return jsonify({'status': False, 'error': "Unknown storage error. Operation failed."})

            return jsonify({'status': True, 'message': "Timer %s deleted" % timer_code})




timer_api_view = TaskListApi.as_view('admin_api')

app.add_url_rule('/timer/<string:timer_code>/', view_func=timer_api_view, methods=['GET', 'POST', 'PUT', 'DELETE'])
app.add_url_rule('/timer/', view_func=timer_api_view, methods=['POST', ], defaults={'timer_code': None})