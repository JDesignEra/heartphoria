from flask import Blueprint, g, render_template, request

from heartphoria.db import get_db

blueprint = Blueprint('general', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    reminders = None
    appointments = None
    bmi = {}

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
        db = get_db()

        reminders = db.execute('SELECT * FROM reminder WHERE user_id = ? ORDER BY time LIMIT 5', [g.user['id']]).fetchall()
        appointments = db.execute('SELECT * FROM appointment WHERE user_id = ? AND date_time > datetime("now") ORDER BY date_time DESC LIMIT 5', [g.user['id']]).fetchall()

    return render_template('index.html', title='Home Page', reminders=reminders, appointments=appointments, bmi=bmi)
