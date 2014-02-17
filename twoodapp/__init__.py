# coding: utf-8
__author__ = 'petrmatuhov'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# load config
import settings

# init app
app = Flask(__name__)
app.config.from_object(settings)

# start db
db = SQLAlchemy(app)


# api entry points
from flask.views import View, MethodView

class TaskListApi(MethodView):
    #get list
    def get(self, timer_code):
        return 'tasklist get %s\n' % timer_code

    # create
    def post(self, timer_code):
        return 'tasklist post %s\n' % timer_code

    #update
    def put(self, timer_code):
        return 'tasklist put %s\n' % timer_code

    # remove
    def delete(self, timer_code):
        return 'tasklist delete %s\n' % timer_code

tasklist_api_view = TaskListApi.as_view('admin_api')
app.add_url_rule('/timer/<string:timer_code>/', view_func=tasklist_api_view, methods=['GET', ])
app.add_url_rule('/timer/<string:timer_code>/', view_func=tasklist_api_view, methods=['POST', ])
app.add_url_rule('/timer/<string:timer_code>/', view_func=tasklist_api_view, methods=['PUT', ])