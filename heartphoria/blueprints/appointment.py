from datetime import datetime

from flask import Blueprint, g, redirect, render_template, request, url_for

from heartphoria import db
from heartphoria.models import Appointment
from heartphoria.blueprints.auth import login_required

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
            appointment = Appointment(user_id=g.user['id'], date_time=date_time, location=location)
            db.session.add(appointment)
            db.session.commit()

            return redirect(url_for('.index'))

    appointments = Appointment.query.filter_by(user_id=g.user['id']).order_by(Appointment.date_time.desc()).all()
    
    return render_template('appointment/index.html', date=date, time=time, location=location, errors=errors, appointments=appointments)
