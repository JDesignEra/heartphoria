from time import sleep
from datetime import datetime, timedelta

import requests
from flask import Blueprint, g, render_template, request

from heartphoria import app
from heartphoria.db import get_db

blueprint = Blueprint('hospital', __name__, url_prefix='/hospital')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    flag = True
    db = get_db()

    now = datetime.utcnow().date()
    locations = db.execute('SELECT * FROM hospital ORDER BY name ASC').fetchall()

    if not locations or (now - locations[0]['last_update']) > timedelta(days=1):
        params = {
            'key': app.config.get('GOOGLE_API_KEY'),
            'query': 'Hospital+and+Clinic+in+Singapore',
            'language': 'en',
            'type': 'hospital,health,establishment,point_of_interest'
        }

        while flag:
            r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json', params=params)
            results = r.json()

            if 'next_page_token' not in results:
                flag = False
            else:
                params['pagetoken'] = results['next_page_token']

            for result in results['results']:
                data = {
                    'id': result['place_id'],
                    'last_update': now,
                    'name': result['name'],
                    'address': result['formatted_address'],
                    'lat': result['geometry']['location']['lat'],
                    'lng': result['geometry']['location']['lng']
                }

                if db.execute('SELECT * FROM hospital WHERE id = ?', [data['id']]).fetchone() is None:
                    db.execute('INSERT INTO hospital (' + ', '.join(k for k in data) + ') VALUES (' + ', '.join('?' for _ in data) + ')', [v for k, v in data.items()])
                else:
                    db.execute('UPDATE hospital SET ' + ', '.join(k + ' = ?' for k in data) + ' WHERE id = ?', [v for k, v in data.items()] + [data['id']])

            db.commit()
            sleep(2)    # Google Places API doesn't allow next result to be called instantly.

        locations = db.execute('SELECT * FROM hospital ORDER BY name ASC').fetchall()

    return render_template('hospital/index.html', title='Hospital Locations', locations=locations, token=app.config.get('MAPBOX_ACCESS_TOKEN'))
