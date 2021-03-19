from githubclient.models import Tags
from githubclient.models import Repository

def test_new_tag():
    tag = Tags(name='Frontend', id_github_account='123456')
    assert tag.name == 'Frontend'
    assert tag.id_github_account == '123456'

def test_new_repository():
    tag = Repository(
        id_repo='123', 
        id_github_account='123456', 
        name='steniols/repositorio-de-testes', 
        description='Este é um repositório de testes',
        url='https://github.com/steniols/repositorio-de-testes',
        stars='3'
    )
    assert tag.name == 'steniols/repositorio-de-testes'
    assert tag.url == 'https://github.com/steniols/repositorio-de-testes'