import datetime
from flask_mongoengine import MongoEngine
from flask.ext.login import UserMixin
from . import login_manager

db = MongoEngine()

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

class User(UserMixin,db.Document):
    username = db.StringField(max_length=25, required=True, unique=True)
    password = db.StringField()
    email = db.StringField(required=True, unique=True)

@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()
