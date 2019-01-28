from datetime import datetime

from flask import Blueprint, g, render_template, request, url_for

from heartphoria import db, redirect
from heartphoria.models import Reminder
from heartphoria.blueprints.auth import login_required

blueprint = Blueprint('reminder', __name__, url_prefix='/reminder')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    time = None
    medication = None
    quantity = None
    errors = {}

    if request.method == 'POST':
        delete = request.form.get('delete')

        if delete:
            reminder = Reminder.query.get(delete)
            db.session.delete(reminder)
            db.session.commit()

            return redirect(url_for('.index'))
        else:
            time = request.form.get('time')
            medication = request.form.get('medication')
            quantity = request.form.get('quantity')

            if not time:
                errors['time'] = 'Time is required.'
            else:
                time = datetime.strptime(time, '%H:%M').time().isoformat()

            if not medication:
                errors['medication'] = 'Medication is required.'

            if not quantity:
                errors['quantity'] = 'Quantity is required.'

            if not errors:
                reminder = Reminder(user_id=g.user['id'], time=datetime.strptime(time, '%H:%M:%S').time(), medication=medication, quantity=quantity)
                db.session.add(reminder)
                db.session.commit()

                return redirect(url_for('.index'))

    reminders = Reminder.query.filter_by(user_id=g.user['id']).all()

    return render_template('reminder/index.html', title='Medication Reminder', time=time, medication=medication, quantity=quantity, errors=errors, reminders=reminders)
