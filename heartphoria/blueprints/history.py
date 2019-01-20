from flask import Blueprint, g, render_template, request

from heartphoria.blueprints.auth import login_required
from heartphoria.db import get_db

blueprint = Blueprint('history', __name__, url_prefix='/history')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    date = None
    description = None
    errors = {}

    db = get_db()

    if request.method == 'POST':
        date = request.form.get('date')
        description = request.form.get('description')

        if not date:
            errors['date'] = 'Date is required.'

        if not description:
            errors['description'] = 'Description is required.'

        if not errors:
            db.execute('INSERT INTO history (user_id, date, description) VALUES (?, ?, ?)',
                       [g.user['id'], date, description])
            db.commit()

    histories = db.execute('SELECT * FROM history WHERE user_id = ? ORDER BY date DESC', [g.user['id']]).fetchall()

    return render_template('history/index.html', title='Medical History', date=date, description=description, errors=errors, histories=histories)
