from datetime import datetime

from flask import Blueprint, g, redirect, render_template, request, url_for

from heartphoria.blueprints.auth import login_required
from heartphoria.db import get_db

blueprint = Blueprint('appointment', __name__, url_prefix='/appointment')

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    date = None
    time = None
    location = None
    errors = {}

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')

        db = get_db()

        if not (date and time):
            if not date:
                errors['date'] = 'Date is required.'

            if not time:
                errors['time'] = 'Time is required.'
        else:
            date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

        if not location:
            errors['location'] = 'Location is required.'

        if not errors:
            db.execute('INSERT INTO appointment (user_id, date_time, location) VALUES (?, ?, ?)', [g.user['id'], date_time, location])
            db.commit()

            return redirect(url_for('.index'))

    appointments = get_db().execute('SELECT * FROM appointment WHERE user_id = ? ORDER BY date_time DESC', [g.user['id']]).fetchall()

    return render_template('appointment/index.html', date=date, time=time, location=location, errors=errors, appointments=appointments)
