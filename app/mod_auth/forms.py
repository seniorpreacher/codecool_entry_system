from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, EqualTo
from peewee import *
from app.mod_auth.models import Visitor
import wtforms


class LoginForm(Form):

    name = wtforms.TextField('Email Address', [Required(message='You must enter a username to sign in.')])
    password = PasswordField('Password', [Required(message='You must provide a password to sign in.')])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        try:
            user = Visitor.get(name=self.name.data)
        except DoesNotExist:
            self.name.errors.append('Unknown username')
            return False

        if user.password != self.password.data:
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
