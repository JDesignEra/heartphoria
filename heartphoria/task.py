import datetime

import requests
from celery import Celery
from kombu import exceptions, Connection

from heartphoria import app
from heartphoria.db import get_db
from heartphoria.mail import mail

def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['result_backend'],
                    broker=app.config['broker_url'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


def check_celery_worker_status():
    errors = {}

    try:
        conn = Connection(app.config['broker_url'])
        conn.ensure_connection(max_retries=1)

    except exceptions.OperationalError as e:
        errors = {'connection': str(e)}

    if not errors:
        workers = celery.control.inspect().active()

        if not workers:
            errors = {'workers': 'No active workers.'}

    return errors


@celery.task()
def celery_send_mail(to, subject, content):
    with app.app_context():
        mail(to, subject, content)


@celery.task()
def update_weather():
    db = get_db()

    now = datetime.now().replace(microseond=0, second=0, minute=0)
    last_update = db.execute('SELECT last_update FROM weather').fetchone()

    # TODO: correct now > last_update check formula
    if not last_update or now > last_update:
        params = {'apikey': 'nKfuTA6IWpYjFarfaEKhWms2yArOwbpq', 'language': 'en-sg', 'details': 'true'}
        r = requests.get('http://dataservice.accuweather.com/currentconditions/v1/300597', params=params)
        result = (r.json())[0]

        weather = {
            'last_update': now,
            'weather_text': result['WeatherText'],
            'weather_icon': result['WeatherIcon'],
            'temperature': result['Temperature']['Metric']['Value'],
            'feel_temperature': result['RealFeelTemperature']['Metric']['Value'],
            'humidity': result['RelativeHumidity'],
            'dew_point': result['DewPoint']['Metric']['Value'],
            'wind_direction': result['Wind']['Direction']['Degrees'],
            'wind_direction_text': result['Wind']['Direction']['English'],
            'wind_speed': result['Speed']['Metric']['Value'],
            'uv_index': result['UvIndex'],
            'uv_index_text': result['UVIndexText'],
            'visibility': result['Visibility']['Metric']['Value'],
            'cloud_cover': result['CloudCover'],
            'pressure': result['Pressure']['Metric']['Value']
        }

        if last_update:
            db.execute('UPDATE weather SET ' + ', '.join(k + ' = ?' for k in weather), [v for k, v in weather.items()])
        else:
            db.execute('INSERT INTO weather (' + ', '.join(k for k in weather) + ') VALUES (' + ', '.join(v for k, v in weather.items()) + ')')
