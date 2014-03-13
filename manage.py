# coding: utf-8
from twoodapp import app, db, manager
from twoodapp.models import *


if __name__ == '__main__':
    db.init_app(app)
    manager.run()
