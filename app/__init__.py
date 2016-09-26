# Import flask and template operators
from flask import Flask, render_template
import sqlite3
from peewee import *

db = SqliteDatabase('users.db')

from app.mod_auth.models import *
from app.mod_xls.models import *

users = [{"name": "admin", "password": "admin"}, {"name": "admin2", "password": "admin2"}]
db.connect()
db.drop_tables([Visitor, Book], safe=True)
db.create_tables([Visitor, Book], safe=True)


with db.atomic():
    Visitor.insert_many(users).execute()

app = Flask(__name__)
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_auth.controllers import mod_auth as auth_module

app.register_blueprint(auth_module)

from app.mod_xls.controllers import mod_xls as xls_module

app.register_blueprint(xls_module)

from app.mod_bulk.controllers import mod_bulk as bulk_module

app.register_blueprint(bulk_module)
