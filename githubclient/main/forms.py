from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length


class SearchForm(FlaskForm):
    search = StringField(
        "Campo da pesquisa",
        validators=[
            Length(
                max=40, message="A pesquisa deve conter no máximo %(max)d caracteres"
            )
        ],
        render_kw={"placeholder": "Pesquise pelo repositório ou tag..."},
    )
    submit = SubmitField("Pesquisar")
