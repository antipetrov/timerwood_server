# coding: utf-8
__author__ = 'petrmatuhov'

SECRET_KEY = 'ssshhhh'
DEBUG = True
SQLALCHEMY_DATABASE_URI = "mysql::timer_user:timer_password@localhost/timerwood"



try:
    from settings_local import *
except:
    pass