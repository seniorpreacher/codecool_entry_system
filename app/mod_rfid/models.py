from peewee import *
import sqlite3
from app import db


class BaseModel(Model):
    """ Peewee models will inherit this base class. """

    class Meta:
        database = db


class Student(BaseModel):
    """ Students, whose name and rfid number are stored in this model, are added to each rfid read event.  """

    name = CharField()
    rfid_id = CharField(null=True)
    last_seen = DateTimeField(null=True)


class Reads(BaseModel):
    """ Stores rfid read events with a timestamp and a corresponding Student model instance. """

    time = DateTimeField()
    student = ForeignKeyField(Student)
