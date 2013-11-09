# coding: utf-8
__author__ = 'petrmatuhov'

from twoodapp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), index=True, unique=True)
    code = db.Column(db.String(64), index=True, unique=True)

class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'))
    edit_time = db.Column(db.DateTime, index=True)
    ord = db.Column(db.Integer, index=True)
    value = db.Column(db.Text)