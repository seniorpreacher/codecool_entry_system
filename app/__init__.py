# Import flask and template operators
from flask import Flask, render_template
import sqlite3
from peewee import *

db = SqliteDatabase('users.db')

from app.mod_auth.models import *
from app.mod_rfid.models import *

users = [{"name": "admin", "password": "admin"}]
students = [
    {"name": "Al", "rfid_id": "egy"}, {"name": "Peggy", "rfid_id": "kettő"},
    {"name": "Kelly", "rfid_id": "három"}, {"name": "Bud", "rfid_id": "négy"},
    {"name": "Bruno", "rfid_id": "öt"}
    ]

db.connect()
db.drop_tables([Admin, Student], safe=True)
db.create_tables([Admin, Student], safe=True)


with db.atomic():
    Admin.insert_many(users).execute()
    Student.insert_many(students).execute()

app = Flask(__name__)
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_auth.controllers import mod_auth as auth_module

app.register_blueprint(auth_module)

from app.mod_rfid.controllers import mod_rfid as rfid_module

app.register_blueprint(rfid_module)
