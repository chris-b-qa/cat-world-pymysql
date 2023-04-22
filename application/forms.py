#!/usr/bin/python

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from application.database import db


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Add User')


class CatForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    owner_id = SelectField('Owner', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Cat')

    def update_owners(self):
        self.owner_id.choices = CatForm.__get_users()

    @classmethod
    def __get_users(cls):
        with db.cursor() as cursor:
            sql_query = 'select id, name from user'
            cursor.execute(sql_query)
            users = list(cursor.fetchall())
            return [(user['id'], user['name']) for user in users]


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class EditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Save changes')
