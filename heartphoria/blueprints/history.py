from flask import Blueprint, g, redirect, render_template, request, url_for

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

    histories = db.execute('SELECT * FROM history WHERE user_id = ? ORDER BY date DESC', [g.user['id']]).fetchall()

    return render_template('history/index.html', date=date, description=description, errors=errors, histories=histories)
