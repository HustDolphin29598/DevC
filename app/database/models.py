import mongoengine as me
from flask_mongoengine import MongoEngine
from mongoengine.fields import StringField, DateField, ListField, IntField, ObjectIdField, EmbeddedDocumentField, ReferenceField
from .db import mongoEngine

class Campaign(mongoEngine.Document):
    _id = ObjectIdField()
    name = StringField(required=True)
    description = StringField()
    startTime = DateField(required=True)
    endTime = DateField(required=True)
    keyword = StringField(required=True)
    links = ListField(mongoEngine.StringField())
    total_comments = IntField()
    total_pos = IntField()
    total_neg = IntField()
    total_neu = IntField()
    status = StringField(required=True)

class Comment(mongoEngine.Document):
    _id = ObjectIdField()
    text = StringField(required=True)
    post_id = StringField()
    label = StringField()

class Post(mongoEngine.Document):
    _id = ObjectIdField()
    post_id = StringField()
    campaign = StringField()
    source = StringField()
    comments_num = StringField()
    date = StringField()
    comments = ListField(StringField())
    url = StringField()
    text = StringField()
    reactions = IntField()
    like = IntField()
    love = IntField()
    haha = IntField()
    wow = IntField()
    sad = IntField()
    care = IntField()