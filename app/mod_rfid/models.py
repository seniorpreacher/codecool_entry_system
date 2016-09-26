from peewee import *
import sqlite3
from app import db


class BaseModel(Model):

    class Meta:
        database = db


class Student(BaseModel):

    name = CharField()
    rfid_id = CharField(null=True)
    last_seen = DateTimeField(null=True)


class Reads(BaseModel):

    time = DateTimeField()
    student = ForeignKeyField(Student)
