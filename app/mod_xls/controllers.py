from flask import Blueprint, render_template
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.mod_xls.processer import FileProcesser

mod_xls = Blueprint('xls', __name__, url_prefix='/xls')

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploads"
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@mod_xls.route('/valami', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processer = FileProcesser(UPLOAD_FOLDER + "/" + filename)
            processer.add_to_database()
            return render_template('index.html')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
