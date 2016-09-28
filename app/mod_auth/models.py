from peewee import *
import sqlite3
from app import db
from flask_login import UserMixin


class BaseModel(Model):
    """ Peewee models will inherit this base class. """
    class Meta:
        database = db


class Admin(BaseModel):
    """ Instances of this class can authenticate through the login page. """
    name = CharField()
    password = CharField()


class User(UserMixin):
    """ Class used to track logged in users. """
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return ("User id: {}".format(self.id))
