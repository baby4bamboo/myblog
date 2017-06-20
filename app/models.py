import datetime
from flask_mongoengine import MongoEngine
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

class User(UserMixin,db.DynamicDocument):
    email = db.StringField(required=True, unique=True)
    password = db.StringField()
    password_hash = db.StringField(max_length=128,default='')
    username = db.StringField(max_length=25, required=True, unique=True)
    group = db.StringField(default='normal', choices=["admin", "editor", "normal"])

    def generate_password_hash(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Document):
    post_id = db.StringField()
    title = db.StringField(max_length=120, required=True)
    author = db.StringField()
    author_id = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField()
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    url = db.StringField()

    meta = {'allow_inheritance': True}

class Comment(db.Document):
    author = db.StringField()
    author_id = db.ReferenceField(User)
    post_id = db.StringField()
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    content = db.StringField()

@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()
