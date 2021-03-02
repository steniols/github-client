from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from githubclient.models import Tags
from flask_dance.contrib.github import github

class TagsForm(FlaskForm):
    origin_name = HiddenField()
    name = StringField('Nome da tag', validators=[
                            DataRequired(message='Campo obrigatório'), 
                            Length(min=2, max=40, message='A tag deve conter pelo menos %(min)d e no máximo %(max)d caracteres')
                        ])
    submit = SubmitField('Salvar')

    def validate_name(self, name,):

        if github.authorized:
            github_account_info = github.get('/user')
            if github_account_info.ok:
                github_account_info_json = github_account_info.json()
                tag = Tags.query.filter_by(name=name.data, id_github_account=github_account_info_json['id']).first()
                if tag and name.data != self.origin_name.data:
                    raise ValidationError('Já existe uma tag com este nome, por favor escolha outro.')