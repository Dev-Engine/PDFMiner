"""."""
# -*- coding: utf-8 -*-
import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    """."""

    name = db.StringField(max_length=50, required=True)
    password = db.StringField()
    email = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)


class Project(db.Document):
    """."""

    name = db.StringField(required=True)
    pdfs = db.SortedListField(db.EmbeddedDocumentField('PdfEm'))
    author = db.ReferenceField(User)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)


class PdfEm(db.EmbeddedDocument):
    """."""

    name = db.StringField(required=True)
    author = db.ReferenceField(User)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
