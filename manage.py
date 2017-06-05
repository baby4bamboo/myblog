#!/usr/bin/env python
import os
from app import create_app
from app.models import User, Todo
from flask.ext.script import Manager, Shell

app = create_app('default')
manager = Manager(app)


from app.models import db
db.init_app(app)

if __name__ == '__main__':
    manager.run()
