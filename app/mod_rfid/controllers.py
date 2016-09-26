from flask import Blueprint, request, render_template
from app import db
from app.mod_rfid.models import Student, Reads

mod_rfid = Blueprint('rfid', __name__, url_prefix='/rfid')


@mod_rfid.route('/')
def index():
    events = Reads.select()
    for event in Reads.select():
        print(event.event)
        print(event.name)
        print(event.rfid_id)
    titles = ["Time", "Name", "RFID ID"]
    return render_template("index.html", events=events, titles=titles)


@mod_rfid.route('/students')
def student_list():
    students = Student.select()
    titles = ["Name", "RFID ID", "Last Seen"]
    return render_template("students.html", students=students, titles=titles)
