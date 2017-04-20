from flask import Flask, render_template
import sqlite3
from peewee import *
from flask_login import LoginManager

db = SqliteDatabase('users.db')

from app.mod_auth.models import *
from app.mod_rfid.models import *

users = [{"name": "admin", "password": "admin"}]
students = [
    {"name": "Daniel Salamon", "rfid_id": "0270318977"},
    {"name": "Peggy", "rfid_id": "kettő"},
    {"name": "Kelly", "rfid_id": "három"},
    {"name": "Bud", "rfid_id": "négy"},
    {"name": "Bruno", "rfid_id": "öt"},
    {"name": "Marcy D'Arcy", "rfid_id": "0269792673"},
    {"name": "Unknown RFID ID", "rfid_id": ""},
    {"name": "Anna Kertész", "rfid_id": "0269794721"}
    ]

db.connect()
#db.drop_tables([Admin, Student, Reads], safe=True)
#db.create_tables([Admin, Student, Reads], safe=True)


#with db.atomic():
#    Admin.insert_many(users).execute()
#    Student.insert_many(students).execute()

app = Flask(__name__)
app.config.from_object('config')
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_auth.controllers import mod_auth as auth_module

app.register_blueprint(auth_module)

from app.mod_rfid.controllers import mod_rfid as rfid_module

app.register_blueprint(rfid_module)
