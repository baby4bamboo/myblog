import datetime
from flask_mongoengine import MongoEngine
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

class User(UserMixin,db.Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField()
    password_hash = db.StringField(max_length=128,default='')
    username = db.StringField(max_length=25, required=True, unique=True)

    def generate_password_hash(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()
