from datetime import datetime, timedelta
from flask import Blueprint, g, render_template, request

import requests

from heartphoria import app
from heartphoria.db import get_db

blueprint = Blueprint('general', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    reminders = None
    appointments = None
    bmi = {}

    db = get_db()

    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    weather = db.execute('SELECT * FROM weather LIMIT 1').fetchone()

    if weather is None or (now - weather['last_update']) > timedelta(hours=1):
        params = {
            'apikey': app.config.get('ACCUWEATHER_API_KEY'),
            'language': 'en-sg',
            'details': 'true'
        }

        r = requests.get('http://dataservice.accuweather.com/currentconditions/v1/300597', params=params)
        results = (r.json())[0]

        data = {
            'last_update': now,
            'weather_text': results['WeatherText'],
            'weather_icon': results['WeatherIcon'],
            'temperature': results['Temperature']['Metric']['Value'],
            'feel_temperature': results['RealFeelTemperature']['Metric']['Value'],
            'humidity': results['RelativeHumidity'],
            'dew_point': results['DewPoint']['Metric']['Value'],
            'wind_direction': results['Wind']['Direction']['Degrees'],
            'wind_direction_text': results['Wind']['Direction']['English'],
            'wind_speed': results['Wind']['Speed']['Metric']['Value'],
            'uv_index': results['UVIndex'],
            'uv_index_text': results['UVIndexText'],
            'visibility': results['Visibility']['Metric']['Value'],
            'cloud_cover': results['CloudCover'],
            'pressure': results['Pressure']['Metric']['Value'],
            'pressure_tendency': results['PressureTendency']['LocalizedText']
        }

        if weather is None:
            db.execute('INSERT INTO weather (' + ', '.join(k for k in data) + ') VALUES (' + ', '.join('?' for _ in data) + ')', [v for k, v in data.items()])

            weather = data
        else:
            db.execute('UPDATE weather SET ' + ', '.join(k + ' = ?' for k in data), [v for k, v in data.items()])

        db.commit()

    if request.method == 'POST' or g.user and g.user['weight'] and g.user['height']:
        bmi = {
            'weight': int(request.form.get('weight') if request.form.get('weight') else g.user['weight']),
            'height': int(request.form.get('height') if request.form.get('height') else g.user['height']),
        }

        bmi['index'] = round(bmi['weight'] / (bmi['height'] / 100 * bmi['height'] / 100))

        if bmi['index'] >= 27.5:
            bmi['text'] = 'HIGH RISK'
        elif bmi['index'] >= 23:
            bmi['text'] = 'MODERATE RISK'
        elif bmi['index'] >= 18.5:
            bmi['text'] = 'LOW RISK'
        else:
            bmi['text'] = 'Risk Of Nutritional Deficiency'

    if g.user:
        reminders = db.execute('SELECT * FROM reminder WHERE user_id = ? ORDER BY time LIMIT 5', [g.user['id']]).fetchall()
        appointments = db.execute('SELECT * FROM appointment WHERE user_id = ? AND date_time > datetime("now") ORDER BY date_time DESC LIMIT 5', [g.user['id']]).fetchall()

    return render_template('index.html', reminders=reminders, appointments=appointments, bmi=bmi, weather=weather)
