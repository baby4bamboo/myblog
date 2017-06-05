#!/usr/bin/env python
import os
from app import create_app
from app.models import User, Todo
from flask.ext.script import Manager, Shell

app = create_app('default')
manager = Manager(app)


from app.models import db
db.init_app(app)

from app.main.views import index,pagination,user
app.add_url_rule('/', view_func=index)
app.add_url_rule('/user', view_func=user)
app.add_url_rule('/pagination', view_func=pagination)

if __name__ == '__main__':
    manager.run()
