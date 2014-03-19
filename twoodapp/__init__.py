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



def jsonp_wrap(obj,funcname):

    result = json.dumps(obj)

    if funcname:
        result = "%s(%s)" % (funcname, obj)

    return result


class TaskListApi(MethodView):
    #get list
    def get(self, timer_code):


        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            result = {'status': False, 'error': 'Timer %s not found' % timer_code}
        else:
            result = {'status': True, 'mode': found_code.code_type, 'data': found_code.timer.timer_data}

        jsonp = request.form.get('jsonp', request.args.get('jsonp', None))
        return jsonp_wrap(result,jsonp)

    # create
    def post(self, timer_code):
        import short_url, random, string
        jsonp = request.form.get('jsonp', request.args.get('jsonp', None))


        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if found_code:
            return jsonp_wrap({'status': False, 'error': 'Timer %s already exists' % found_code.code},jsonp)

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




        return jsonp_wrap({
            'status': True,
            'master_code': timer_code,
            'guest_code': guest_code,
        },jsonp)

    #update
    def put(self, timer_code):

        jsonp = request.form.get('jsonp', request.args.get('jsonp', None))

        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            return jsonp_wrap({'status': False, 'error': "Timer not found"}, jsonp)

        if not found_code.code_type == 'master':
            return jsonp_wrap({'status': False, 'error': "Operation not permitted"}, jsonp)
        else:

            new_data = request.form['data']

            timer = found_code.timer

            timer.edit_time = datetime.datetime.now()
            timer.timer_data = new_data

            try:
                db.session.commit()
            except Exception:
                return jsonp_wrap({'status': False, 'error': "Unknown storage error. Operation failed."}, jsonp)

            return jsonp_wrap({'status': True, 'message': "Timer %s updated" % timer_code}, jsonp)

    # remove
    def delete(self, timer_code):

        jsonp = request.form.get('jsonp', request.args.get('jsonp', None))

        # check timer code
        found_code = models.TimerCode.query.filter((models.TimerCode.code == timer_code)).first()

        if not found_code:
            return jsonp_wrap({'status': False, 'error': "Timer not found"}, jsonp)

        if not found_code.code_type == 'master':
            return jsonp_wrap({'status': False, 'error': "Operation not permitted"}, jsonp)
        else:

            timer = found_code.timer

            models.TimerCode.query.filter(models.TimerCode.timer == timer).delete()
            db.session.delete(timer)

            try:
                db.session.commit()
            except Exception:
                return jsonp_wrap({'status': False, 'error': "Unknown storage error. Operation failed."}, jsonp)

            return jsonp_wrap({'status': True, 'message': "Timer %s deleted" % timer_code}, jsonp)




timer_api_view = TaskListApi.as_view('admin_api')

app.add_url_rule('/timer/', view_func=timer_api_view, methods=['POST', ], defaults={'timer_code': None})
app.add_url_rule('/timer/<string:timer_code>/', view_func=timer_api_view, methods=['GET', 'POST', 'PUT', 'DELETE'])


