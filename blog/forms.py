from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired
from blog import db
from werkzeug.routing import ValidationError
from config import Config


class EntryForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    is_published = BooleanField('is_published')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        if field.data != Config.ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    def validate_password(self, field):
        if field.data != Config.ADMIN_PASSWORD:
            raise ValidationError("Invalid password")
        return field.data