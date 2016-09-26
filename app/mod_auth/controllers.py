from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    form = LoginForm()

    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.name)
        session['user_id'] = form.user.id
        return render_template('index.html')

    return render_template("auth/signin.html", form=form)
