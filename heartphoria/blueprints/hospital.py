from time import sleep
from datetime import datetime, timedelta

import requests
from flask import Blueprint, render_template

from heartphoria import app, db
from heartphoria.models import Hospital

blueprint = Blueprint('hospital', __name__, url_prefix='/hospital')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    flag = True

    now = datetime.utcnow().date()
    locations = Hospital.query.order_by(Hospital.name).all()

    if not locations or (now - locations[0].last_update) > timedelta(days=1):
        params = {
            'key': app.config.get('GOOGLE_API_KEY'),
            'query': 'Hospital+and+Clinic+in+Singapore',
            'language': 'en',
            'type': 'hospital,health,establishment,point_of_interest'
        }

        while flag:
            try:
                r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json', params=params, timeout=2)
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

                    if Hospital.query.filter_by(id=data['id']).first() is None:
                        db.session.add(Hospital(**data))
                    else:
                        Hospital.query.filter_by(id=data['id']).update(data)

                db.session.commit()
                sleep(2)    # Google Places API doesn't allow next result to be called instantly.
            except requests.RequestException as e:
                print(e)

        locations = Hospital.query.order_by(Hospital.name).all()

    return render_template('hospital/index.html', title='Hospital Locations', locations=locations, token=app.config.get('MAPBOX_ACCESS_TOKEN'))
