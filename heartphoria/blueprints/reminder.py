from datetime import datetime

from flask import Blueprint, g, redirect, render_template, request, url_for

from heartphoria.blueprints.auth import login_required
from heartphoria.db import get_db

blueprint = Blueprint('reminder', __name__, url_prefix='/reminder')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    time = None
    medication = None
    quantity = None
    errors = {}

    db = get_db()

    if request.method == 'POST':
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
            db.execute('INSERT INTO reminder (user_id, time, medication, quantity) VALUES (?, ?, ?, ?)', [g.user['id'], time, medication, quantity])
            db.commit()

            return redirect(url_for('.index'))

    reminders = db.execute('SELECT * FROM reminder WHERE user_id = ? ORDER BY time', [g.user['id']]).fetchall()

    return render_template('reminder/index.html', title='Medication Reminder', time=time, medication=medication, quantity=quantity, errors=errors, reminders=reminders)
