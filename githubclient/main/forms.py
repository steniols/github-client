from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from githubclient.models import Repository


class SearchForm(FlaskForm):
    search = StringField('Campo da pesquisa', validators=[Length(max=40, message='A pesquisa deve conter no máximo %(max)d caracteres')], render_kw={"placeholder": "Pesquise pelo repositório ou tag..."})
    submit = SubmitField('Pesquisar')