from datetime import datetime, timedelta

import requests
from flask import Blueprint, g, render_template, request

from heartphoria import app, db
from heartphoria.models import Weather, Reminder, Appointment

blueprint = Blueprint('general', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    reminders = None
    appointments = None
    bmi = {}

    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    weather = Weather.query.first()

    if weather is None or (now - weather.last_update) > timedelta(hours=1):
        params = {
            'apikey': app.config.get('ACCUWEATHER_API_KEY'),
            'language': 'en-sg',
            'details': 'true'
        }

        try:
            r = requests.get('http://dataservice.accuweather.com/currentconditions/v1/300597', params=params, timeout=2)
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
                db.session.add(Weather(**data))
                weather = data
            else:
                Weather.query.filter_by(id=1).update(data)

            db.session.commit()
        except requests.exceptions.RequestException as e:
            print(e)

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
        reminders = Reminder.query.filter_by(user_id=g.user['id']).order_by(Reminder.time).limit(5).all()
        appointments = Appointment.query.filter_by(user_id=g.user['id']).filter(Appointment.date_time > datetime.now()).order_by(Appointment.date_time.desc()).limit(5).all()

    return render_template('index.html', reminders=reminders, appointments=appointments, bmi=bmi, weather=weather)
