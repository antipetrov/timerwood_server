# coding: utf-8
__author__ = 'petrmatuhov'

from flask import Flask, jsonify
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
from flask.views import MethodView
from flask import request
import datetime
from flask_cors import cross_origin
from flask.ext.jsonpify import jsonify


class TaskListApi(MethodView):
    #get list
    @cross_origin(methods=settings.api_metods, automatic_options = True)
    def get(self, timer_code):

        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            result = {'status': False, 'error': 'Timer %s not found' % timer_code}
        else:
            if found_code.code_type == 'master':
                # find guest code
                found_guest = models.TimerCode.query.filter((models.TimerCode.timer_id == found_code.timer.id) &
                                                            (models.TimerCode.code_type == 'guest')).first()
                result = {'status': True, 'mode': found_code.code_type, 'guest_code': found_guest.code,
                          'data': found_code.timer.timer_data}
            else:
                result = {'status': True, 'mode': found_code.code_type, 'data': found_code.timer.timer_data}

        return jsonify(result)

    # create
    @cross_origin(methods=settings.api_metods)
    def post(self, timer_code):
        import short_url, random, string
        jsonp = request.form.get('jsonp', request.args.get('jsonp', None))


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

        # add guest code
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
    @cross_origin(methods=settings.api_metods)
    def put(self, timer_code):

        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            return jsonify({'status': False, 'error': "Timer not found"})

        if not found_code.code_type == 'master':
            return jsonify({'status': False, 'error': "Operation not permitted"})
        else:

            new_data = request.form['data']

            timer = found_code.timer

            timer.edit_time = datetime.datetime.now()
            timer.timer_data = new_data

            try:
                db.session.commit()
            except Exception:
                return jsonify({'status': False, 'error': "Unknown storage error. Operation failed."})

            return jsonify({'status': True, 'message': "Timer %s updated" % timer_code})

    # remove
    @cross_origin(methods=settings.api_metods)
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

            try:
                db.session.commit()
            except Exception:
                return jsonify({'status': False, 'error': "Unknown storage error. Operation failed."})

            return jsonify({'status': True, 'message': "Timer %s deleted" % timer_code})

    @cross_origin(methods=settings.api_metods)
    def options (self,timer_code):
        return jsonify({'status': True})


@app.errorhandler(404)
@cross_origin(methods=settings.api_metods)
def error_not_found(e):
    return jsonify({'status': False, 'error': 'Requested URL not found'})

timer_api_view = TaskListApi.as_view('timer_api')

app.add_url_rule('/timer/', view_func=timer_api_view, methods=['POST', ], defaults={'timer_code': None})
app.add_url_rule('/timer/<string:timer_code>/', view_func=timer_api_view,
                 methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])


