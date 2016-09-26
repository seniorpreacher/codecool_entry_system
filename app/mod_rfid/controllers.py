from flask import Blueprint, request, render_template
from app import db
from app.mod_rfid.models import Student

mod_rfid = Blueprint('rfid', __name__, url_prefix='/rfid')


@mod_rfid.route('/')
def index():
    students = Student.select()
    titles = ["Name", "RFID ID", "Last Seen"]
    return render_template("index.html", students=students, titles=titles)
