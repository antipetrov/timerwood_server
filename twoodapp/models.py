# coding: utf-8
__author__ = 'petrmatuhov'

from twoodapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), index=True, unique=True)
    code = db.Column(db.String(64), index=True, unique=True)

class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime(), index=True)
    edit_time = db.Column(db.DateTime(), index=True)
    master_code = db.Column(db.String(64), index=True)
    guest_code =  db.Column(db.String(64), index=True)
    timer_data = db.Column(db.Text)
