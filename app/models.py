import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

class User(db.Document):
    username = db.StringField(max_length=60)
    password = db.StringField(max_length=60)
    gender = db.StringField(default="Male")
