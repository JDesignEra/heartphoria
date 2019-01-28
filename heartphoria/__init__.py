import os
from datetime import datetime

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import find_modules, import_string


app = Flask(__name__)
app.secret_key = b'\xc44\xe9\xaf\x7f\xe0\xd2we\xc8\xbc\xda\x02sm\x16'

app.config['UPLOAD_FOLDER'] = os.getcwd() + '/heartphoria/static/images/dp/'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../heartphoria.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_pyfile('../secrets.conf')

# Celery config, update broker_url & result_backend accordingly if you intend use Celery.
app.config.update(
    broker_url='amqp://heartphoria:password@localhost:5672/heartphoria',
    result_backend='rpc://',
    broker_heartbeat=0,
    task_serializer='json',
    accept_content=['json'],
    timezone='Asia/Singapore',
    enable_utc=True
)

from heartphoria import database
database.init_app()

db = SQLAlchemy(app)

# Change URL accordingly if using ngrok otherwise you may ignore it.
ngrok_url = 'https://heartphoria.ap.ngrok.io'


# Checks if ngrok tunnel is up.
# If ngrok tunnel is up forced redirect to ngrok domain with https.
# Bypass school internet non-https filter.
def redirect(location, code=302, Response=None):
    import flask

    try:
        if requests.get(ngrok_url, timeout=1).status_code == 200:
            return flask.redirect(ngrok_url + location, code, Response)
        else:
            return flask.redirect(location, code, Response)
    except requests.exceptions.RequestException as e:
        print(e)


@app.context_processor
def year():
    return {'year': datetime.utcnow().year}


for name in find_modules('heartphoria.blueprints'):
    mod = import_string(name)
    if hasattr(mod, 'blueprint'):
        app.register_blueprint(mod.blueprint)
