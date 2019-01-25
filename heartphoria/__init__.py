import os
from datetime import datetime

from flask import Flask, request, redirect
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


@app.context_processor
def year():
    return {'year': datetime.utcnow().year}


for name in find_modules('heartphoria.blueprints'):
    mod = import_string(name)
    if hasattr(mod, 'blueprint'):
        app.register_blueprint(mod.blueprint)


@app.before_request
def http_to_https():
    if request.url.startswith('http://heartphoria.ap.ngrok.io'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, 301)
