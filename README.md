
# Github client

Github client is a phyton tool that allows your users to add tags to their Github repositories.

## Getting Started

First of all it is necessary that you have python 3.9 installed and preferably do the installation of requiriments.txt inside a virtualenv.

```
git clone git@github.com:steniols/github-client.git
cd github-client
cp githubclient/.env.sample githubclient/.env
pip install -r requeriments.txt
```

On [Github's developer settings](https://github.com/settings/developers) create a Oauth APP, it's important to insert your app url in *Homepage URL* and *Authorization callback URL*.
*(for my local development environment, i'm using http://127.0.0.1:5000/)*

This APP will generate a CLIENT_ID and CLIENT_SECRET, we'll update these values on .env file

## Usage

On project root folder just run:

```
python run.py
```

## Tests

```
pytest -v
```

## Live version

http://stenio.pythonanywhere.com/
