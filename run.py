from githubclient import create_app
from socket import gethostname

app = create_app()

if __name__ == '__main__':
    if 'liveconsole' not in gethostname(): 
        app.run(debug=True)