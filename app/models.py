from datetime import datetime
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
    group = db.StringField(default='subscriber', choices=["administrator", "editor", "subscriber"])

    def generate_password_hash(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Document):
    title = db.StringField(max_length=120, required=True)
    author = db.ReferenceField(User)
    content = db.StringField()
    tags = db.ListField(db.StringField(max_length=30))
    #comments = db.ListField(db.EmbeddedDocumentField(Comment))

    meta = {'allow_inheritance': True}

class Comment(db.EmbeddedDocument):
    content = db.StringField()
    name = db.StringField(max_length=120)

@login_manager.user_loader
def user_load(user_id):
    return User.objects(id=user_id).first()
