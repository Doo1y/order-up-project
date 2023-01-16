from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, SelectMultipleField  # noqa
from wtforms.validators import DataRequired, ValidationError
from app import db


class LoginForm(FlaskForm):
    employee_number = StringField('Employee Number', validators=[DataRequired()])  # noqa
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class HostForm(FlaskForm):
    tables = SelectField("Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")


class AddToOrder(FlaskForm):
    menu_item_ids = SelectMultipleField("Menu items", coerce=int)
