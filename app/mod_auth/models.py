from peewee import *
import sqlite3
from app import db
from flask_login import UserMixin


class BaseModel(Model):

    class Meta:
        database = db


class Visitor(BaseModel):
    name = CharField()
    password = CharField()


class User(UserMixin):

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return ("User id: {}".format(self.id))
